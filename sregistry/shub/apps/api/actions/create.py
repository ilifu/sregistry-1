'''

Copyright (C) 2017-2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from shub.settings import MEDIA_ROOT
from sregistry.utils import parse_image_name
from shub.logger import bot
from django.db import IntegrityError
from django.db.utils import DataError
import shutil
import uuid
import json
import os

def move_upload_to_storage(collection, upload_id):
    '''moving an uploaded *UploadImage* to storage means:
         1. create a folder for the collection, if doesn't exist
         2. an image in storage. It will be moved here from
       the temporary upload and renamed
    '''
    from shub.apps.api.models import ImageUpload

    # Get ImageFile instance, rename the file
    instance = ImageUpload.objects.get(upload_id=upload_id)

    # Create collection root, if it doesn't exist
    image_home = "%s/%s" %(MEDIA_ROOT, collection.name)
    if not os.path.exists(image_home):
        os.mkdir(image_home)
    
    # Rename the file, moving from ImageUpload to Storage
    filename = os.path.basename(instance.file.path)
    new_path = os.path.join(image_home, filename.replace('.part', '.simg'))
    shutil.move(instance.file.path, new_path)
    print('%s --> %s' %(instance.file.path, new_path))
    instance.file.name = new_path
    instance.save()
    return instance

def generate_nginx_storage_path(collection, source, dest):
    '''generate the path to move a source to its destination 
       so that we can check length limits, etc., before trying to do the move.
         Parameters
         ==========
         collection: the collection the image will belong to
         source: the source file (under /var/www/images/_upload/{0-9}
         dest: the destination filename
    '''
    image_home = "%s/%s" %(MEDIA_ROOT, collection.name)
    return os.path.join(image_home, os.path.basename(dest))


def move_nginx_upload_to_storage(collection, source, dest):
    '''moving an uploaded file (from nginx module) to storage means.
         1. create a folder for the collection, if doesn't exist
         2. an image in storage pointing to the moved file

         Parameters
         ==========
         collection: the collection the image will belong to
         source: the source file (under /var/www/images/_upload/{0-9}
         dest: the destination filename
    '''
    # Create collection root, if it doesn't exist
    image_home = "%s/%s" %(MEDIA_ROOT, collection.name)
    if not os.path.exists(image_home):
        os.mkdir(image_home)
    
    new_path = os.path.join(image_home, os.path.basename(dest))
    shutil.move(source, new_path)
    return new_path


def upload_container(cid, user, name, version, upload_id, size=None):
    '''save an uploaded container, usually coming from an ImageUpload

       Parameters
       ==========
       cid: the collection id to add the container to
       user: the user that has requested the upload
       upload_id: the upload_id to find the container (for web UI upload)
                  if it exists as a file, an ImageUpload is created instead.
       name: the requested name for the container
       version: the md5 sum of the file

       Returns
       =======
       message: None on successful upload, specific error message. This is 
                a decision because it's purely intended to show to the user,
                if the function is used otherwise we would want these to be
                error / success codes.
    '''

    from shub.apps.main.models import ( Container, Collection )
    from shub.apps.api.models import ( ImageUpload, ImageFile )
    from shub.apps.main.views import update_container_labels
    collection = Collection.objects.get(id=cid)

    # Only continue if user is an owner
    if user in collection.owners.all():

        # parse the image name, get the datafile
        names = parse_image_name(name, version=version)
        storage = os.path.basename(names['storage'])

        # Catch the data error before trying to create it
        new_path = generate_nginx_storage_path(collection, upload_id, storage)

        # Return an error to the user if the file is too big
        if len(new_path) > 255:
            message = 'Filename too long!\nMust be less than 255 characters'
            bot.error(message)
            return message

        # If the path exists, it's a file from nginx module, move to storage
        if os.path.exists(upload_id):

            # If name is too long, will return OSError on move to storage
            new_path = move_nginx_upload_to_storage(collection, upload_id, storage)
            instance = ImageUpload.objects.create(file=new_path)
        else:
            instance = move_upload_to_storage(collection, upload_id)

        image = ImageFile.objects.create(collection=collection,
                                         tag=names['tag'],
                                         name=names['uri'],
                                         owner_id=user.id,
                                         datafile=instance.file)

        # Get a container, if it exists (and the user is re-using a name)
        # Filter by negative id so we get the more recent container first.
        collection_set = collection.containers
        containers = collection_set.filter(tag=names['tag'],
                                           name=names['image']).order_by('-id')

        # If one exists, we check if it's frozen
        create_new = True

        if len(containers) > 0:

            # If we already have a container, it might be frozen
            container = containers[0]

            # If it's not frozen, overwrite the same file
            if container.frozen is False:
                container.delete()
                create_new = False
         
        # Container doesn't already exist / or old version isn't frozen
        if create_new is True:
            try:
                container = Container.objects.create(collection=collection,
                                                     name=names['image'],
                                                     tag=names['tag'],
                                                     image=image,
                                                     version=names['version'])

            # Catches when container is frozen, and version already exists
            except IntegrityError:
                message = '%s/%s:%s@%s already exists.' %(collection.name,
                                                          names['image'],
                                                          names['tag'],
                                                          names['version'])
                bot.error(message)
                delete_file_instance(instance)
                return message

        # Otherwise, use the same container object, but update version
        else:
            container.image = image
            container.version = names['version']
       
        container.save()

        # Save the size
        if size is None:
            size = os.path.getsize(instance.file.path) >> 20
        container.metadata['size_mb'] = size

        # Once the container is saved, delete the intermediate file object
        delete_file_instance(instance)


def delete_file_instance(instance):
    '''a helper function to remove the file assocation, and delete the instance
       if needed outside of this module can be added to models
    '''
    instance.file = None # remove the association
    instance.save()
    instance.delete()
