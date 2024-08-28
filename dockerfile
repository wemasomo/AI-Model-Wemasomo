
####### 👇 OPTIMIZED SOLUTION (x86)👇 #######

# tensorflow base-images are optimized: lighter than python-buster + pip install tensorflow
FROM tensorflow/tensorflow:2.10.0
# OR for apple silicon, use this base image, but it's larger than python-buster + pip install tensorflow
# FROM armswdev/tensorflow-arm-neoverse:r22.09-tf-2.10.0-eigen

WORKDIR /app

# We strip the requirements from useless packages like `ipykernel`, `matplotlib` etc...
COPY Masomo/requirements.txt /app/
RUN RUN pip install --no-cache-dir -r requirements.txt

COPY Masomo /app/Masomo

CMD uvicorn interface.stream_app.fast:app --host 0.0.0.0 --port 8000
# $DEL_END
