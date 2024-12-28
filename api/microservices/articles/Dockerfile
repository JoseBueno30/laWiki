FROM python:3.7 AS builder

WORKDIR /usr/src/app

RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

RUN pip install --upgrade pip
RUN pip install mwparserfromhell
RUN pip install pypandoc_binary

COPY . .
RUN pip install --no-cache-dir .
RUN pip install motor
RUN pip install mwparserfromhell
RUN pip install pypandoc_binary
RUN pip install yagmail


FROM python:3.7 AS test_runner
WORKDIR /tmp
COPY --from=builder /venv /venv
COPY --from=builder /usr/src/app/tests tests
ENV PATH=/venv/bin:$PATH

# install test dependencies
RUN pip install pytest

# run tests
RUN pytest tests


FROM python:3.7 AS service
WORKDIR /root/app/site-packages
COPY --from=test_runner /venv /venv
ENV PATH=/venv/bin:$PATH
