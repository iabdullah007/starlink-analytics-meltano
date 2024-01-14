ARG MELTANO_IMAGE=meltano/meltano:v2.1.0-python3.8
FROM $MELTANO_IMAGE

WORKDIR /projects

# Install any additional requirements
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy over Meltano project directory
COPY . .
RUN meltano install

# Expose default port used by `meltano ui`
EXPOSE 5000

ENTRYPOINT [ "meltano" ]
