# Socless Sumologic

Sumo Logic integrations for the SOCless framework.

# Deployment Instructions

## Prerequisites

- A Sumo Logic account
- Socless Automation Framework deployed in an AWS Account

## Deploy socless-sumologic

Clone this repository to your projects folder using the command below

```
git clone git@github.com:twilio-labs/socless-sumologic.git
```

Change into the `socless-sumologic` repository and setup deployment dependencies by running the commands below

```
npm install
virtualenv venv
. venv/bin/activate
```

## (Optional) Ensure Your Dev/Prod environment matches your Socless Dev/Prod regions

Open the package.json and ensure your `config` and `scripts` match what you have configured for your Socless deployment

## Deploy to Dev and Prod

Deploy your application to dev and prod by running the commands below.
To dev:

```
npm run dev
```

To prod:

```
npm run prod
```

Feel free to deploy to any other Socless environment you have configured

If your Socless deployment is successful, you will see a URL that ends in `/sumologic` in your `endpoints` section. This is your `Sumologic Endpoint URL`.

## Testing

Tests are implemented with `tox` and automatically clean up artifacts if all tests pass:

```
npm run test
```

Tests use the `moto` library to intercept calls to AWS from boto3 and return a mocked event to the tested function.

Tests are implemented using the tox library to create a virtual environment, install dependencies from `functions/requirements.txt` plus test dependencies `moto` and `boto3`, set environment variables needed for the tested functions, and to initiate `pytest`.

`tests/events` folder stores event `.json` files that can be imported when writing test cases or used to test lambda functions directly via AWS console.
