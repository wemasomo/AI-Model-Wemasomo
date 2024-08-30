
####### 👇 OPTIMIZED SOLUTION (x86)👇 #######

# tensorflow base-images are optimized: lighter than python-buster + pip install tensorflow
FROM tensorflow/tensorflow:2.10.0
# OR for apple silicon, use this base image, but it's larger than python-buster + pip install tensorflow
# FROM armswdev/tensorflow-arm-neoverse:r22.09-tf-2.10.0-eigen


# We strip the requirements from useless packages like `ipykernel`, `matplotlib` etc...
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY Masomo Masomo

CMD uvicorn Masomo.api.app:app --host 0.0.0.0 --port $PORT
# $DEL_END
