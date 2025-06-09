## Create virtual environment
```
python -m venv dds_env
```

## Activate virtual environment
```
source dds_env/bin/activate
```

## Install dependencies
```
pip install -r requirements.txt
```


## Create Lambda Layer

1. Create a directory named python
```
mkdir python
```

2. Copy the dependencies to the python directory
```
cp -r dds_env/lib/python3.8/site-packages/* python/
```

3. Zip the python directory
```
zip -r python.zip python/
```

4. Upload the zip file to AWS Lambda Layer