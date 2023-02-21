# download-classifier

Simple python application to classify downloads into folders

- datasets
- documents
- images

The application can be run as a docker container and whenver files are downloaded they will be moved into the respective folders.


# Build

```bash
docker build -t download-classifier .
```

## Test

```bash
docker run -itd --name download-classifier
```

# Development

Create python virtual environment and activate

```bash
python -m venv .venv
source .venv/bin/activate

# When done
deactivate
```
