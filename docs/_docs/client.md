---
title: sregistry client
pdf: true
toc: false
---

# Clients

## Singularity Pull

Singularity Registry Server implements a basic version of the Sylabs Library API, 
meaning that you can pull a container with Singularity directly. For example,
let's say that I have a collection with a container called `collection/container:tag`.
and my registry is served at `containers.page`. I could pull it as follows:

```bash
$ singularity pull --library https://containers.page collection/container:tag
```

You can also pull a container using Singularity natively with the `shub://` uri:

```bash
$ singularity pull shub://containers.page/collection/container:tag
```

# Singularity Registry Client

Singularity Registry Global Client, or [sregistry-cli](https://github.com/singularityhub/sregistry-cli),
is a general client to interact with Singularity images at remote endpoints, and it provides
such an endpoint for Singularity Registry Server. We will provide
basic instructions here, and for the full documentation, please see the [getting started guide here](https://singularityhub.github.io/sregistry-cli/client-registry). Note that you will need to [export your credentials](https://singularityhub.github.io/sregistry/credentials) in order to have authenticated interaction with sregistry.


## Install

### sregistry Installation

`sregistry` is the client for Singularity Registry server. To install, you can do the following:

```bash
git clone https://github.com/singularityhub/sregistry-cli
cd sregistry-cli
python setup.py install
```

To check your install, run this command to make sure the `sregistry` client is found.

which sregistry


### Container Install

We have provided a Singularity build definition for you, for which you can use to build a container that serves as the sregistry client (and this will likely be provided on Singularity Hub so you don't even need to do that.) To build, do the following:

```bash
cd sregistry/

# Singularity 2.4 and up
sudo singularity build sregistry Singularity

# For Singularity earlier than 2.4 (deprecated)
singularity create --size 2000 sregistry
sudo singularity bootstrap sregistry Singularity
```

If you install via this option, you will want to make sure the container itself is somewhere on your path, with appropriate permissions for who you want to be able to use it.


## Commands
This brief tutorial assumes that you have [Singularity installed](https://singularityware.github.io/install-linux).

### Pull
Not shown in the demo above is the pull command, but it does the same thing as the singularity pull.

```bash
sregistry pull banana/pudding:milkshake
Progress |===================================| 100.0% 
Success! banana-pudding-milkshake.img
```

This is useful so that you can (locally from your registry) pull an image without needing to specify the registry url. It's also important because registry support will only be added to Singularity when the entire suite of compoenents are ready to go!


### Push

If you don't have an image handy, you can pull one from Singularity Hub:

```bash
singularity pull shub://vsoch/hello-world
```

And then a push to your registry looks like this:

```bash
sregistry push vsoch-hello-world-master.img --name dinosaur/avocado --tag delicious
sregistry push vsoch-hello-world-master.img --name meowmeow/avocado --tag nomnomnom
sregistry push vsoch-hello-world-master.img --name dinosaur/avocado --tag whatinthe
```

If you don't specify a tag, `latest` is used. If you have authentication issues,
remember that you need to [export a token](https://singularityhub.github.io/sregistry/credentials) for your user, and ensure that the user is either an admin/manager, or
that you have set the `USER_COLLECTIONS` variable to true. You can read [more about roles here](https://singularityhub.github.io/sregistry/setup-roles), and [more about teams](https://singularityhub.github.io/sregistry/setup-teams) to manage groups of people.

### List

List is a general command that will show a specific container, a specific collection, optionally with a tag. Examples are provided below:

```bash
# All collections
sregistry list

# A particular collection
sregistry list dinosaur

# A particular container name across collections
sregistry list /avocado

# A named container, no tag
sregistry list dinosaur/avocado

# A named container, with tag
sregistry list dinosaur/avocado:delicious
```

In addition to listing containers, `sregistry` can show you metadata! It does this by issuing an inspect command at upload time, so that no processing is needed on the server side. Singularity Registry is a Dockerized application, so it would require --privileged mode, which is a bad idea. Anyway, we can look at environment (`--env/-e`), runscript (`--runscript/-r`), tests (`--test/-t`), or `Singularity` definition recipe (`--deffile/-d`):

```bash
# Show me environment
sregistry list dinosaur/tacos:delicious --env

# Add runscript
sregistry list dinosaur/tacos:delicious --e --r

# Definition recipe (Singularity) and test
sregistry list dinosaur/tacos:delicious --d --t

# All of them
sregistry list dinosaur/tacos:delicious --e --r --d --t
```

### Delete
Delete requires the same authentication as push, and you will need to confirm with `yes/no`

```bash
sregistry delete dinosaur/tacos:delicious
sregistry list
```

if you want to force it, add `--force`

```bash
sregistry delete dinosaur/tacos:delicious --force
```

### Labels
Labels are important, and so they are represented as objects in the database for index, query, etc. Akin to containers, we can list and search:

```bash
# All labels
sregistry labels

# A specific key
sregistry labels --key maintainer

# A specific value
sregistry labels --value vanessasaur

# A specific key and value
sregistry labels --key maintainer --value vanessasaur
```
