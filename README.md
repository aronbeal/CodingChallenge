# README

This is the provided solution by Aron Beal to the BusPatrol coding challenge.  For details of the challenge, please see [Instructions](./Instructions.md).  It uses the python [unittest](https://docs.python.org/3/library/unittest.html) library for testing.

## Running Locally

To run this container locally:

1. Ensure you are running OSX (only tested platform so far).
2. Ensure you are running the Docker daemon locally.
3. Clone the project from repository, and open a terminal window to the repo root.
4. Run the command `docker compose build` to build all requisite docker containers.
5. Run the command `docker compose up -d` to start the API stack in the background.
6. Open a browser window to <http://127.0.0.1:5000/>.  You should see a plain html page enumerating the various routes.
7. Connect to the running api container by executing `docker compose exec -it bash`.
8. Run `docker compose down` when you are done to shut down the stack, and clean up docker resources used.

## Debugging

The endpoint <http://127.0.0.1:5000/debug> is available to obtain information about the setup locally.  This endpoint should NOT be made available in a production environment, but for purposes of this exercise, was deemed ok and useful.

## Testing

TODO
