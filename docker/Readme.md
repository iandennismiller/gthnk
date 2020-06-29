# docker-gthnk

## Quick start

The following commands will do the following:

1. Launch the Gthnk Docker image
2. Initialize the database
3. Add a new user to Gthnk

```
docker run -d --rm \
    --name gthnk \
    -p 1620:1620 \
    -v ~/.gthnk:/home/gthnk/storage \
    iandennismiller/gthnk
```

Once Gthnk is running, connect at http://localhost:1620 and log in with the username `user@example.com` and the password `secret`.

This will create a folder in your home directory called `.gthnk` that contains a configuration file, database, and log file.
You can use `~/.gthnk/gthnk.conf` file to control how Gthnk operates.

## Administration

### Stopping Gthnk

```
docker stop gthnk
```

### Create an account

You can create an account with an email address and password:

```
docker exec -it gthnk \
    sudo -i -u gthnk \
    gthnk-user-add.sh EMAIL PASSWORD
```

### Delete an account

The docker image has the account `user@example.com` already on it.
You can delete that account by running the following:

```
docker exec -it gthnk \
    sudo -i -u gthnk \
    gthnk-user-del.sh user@example.com
```
