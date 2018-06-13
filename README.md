# S4S Testsuite

Framework for testing S4S API implementations. The interface is a [Flask](http://flask.pocoo.org/) application, and the tests themselves are run as [Celery](http://www.celeryproject.org/) tasks. The tests are written using the [behave](http://behave.readthedocs.io/en/stable/index.html) framework.

## Build and run in Docker

We use [Docker](https://www.docker.com/) to set up all the required services and run the test server.

    git clone https://github.com/sync-for-science/test-suite
    cd test-suite
    docker build -t tests .
    docker run --rm -it \
      -p 9003:5000 \
      tests

`9003` is the default port, but you can configure it to run on other ports - just be sure to add `-e BASE_URL=http://localhost:<port>` to the Docker command as well.
      
### Develop in Docker

If you want to develop on the app using Docker, mount the repository on the container. Note that the container still has to be restarted to reflect any changes.

    docker run --rm -it \
      -p 9003:5000 \
      -v /host/path/to/test-suite:/usr/src/app \
      tests

### Building the js app (for development)

Install [npm](https://www.npmjs.com/), then `npm install` and `npm run-script build`. If you're editing
JS, you can run `npm run-script watch` to automatically re-build when files
change.

## Bloom filter

The test suite uses a [Bloom filter](https://en.wikipedia.org/wiki/Bloom_filter) to validate known codes. The filter is built with the `data/build_bf.py` script, but requires a number of external databases to be downloaded first. As a convenience, we maintain a prebuilt filter, which is downloaded every time the container starts.

## Running the test suite

Navigate to `http://localhost:9003/` (or whichever port you've selected), then select the vendor you'd like to test and the types of test you'd like to perform, and optionally any custom configuration as outlined [here](config/README.md). The tests are run as Celery tasks, and the interface is updated in realtime as the results are ready.

## Testing the test suite

To test the... test suite, use py.test

```
pip install -e . # Install "testsuite" so that the tests can find it
py.test
```

To see see test coverage, generate a coverage report and navigate to
/static/coverage/index.html.

```
py.test --cov=testsuite --cov-report html
```
