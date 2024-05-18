#!/bin/bash

# Define an array of regions where your Lambda functions are deployed
REGIONS=("us-east-1" "us-west-2" "eu-central-1") # add more regions as required

# Loop through each region
for REGION in "${REGIONS[@]}"
do
  echo "Processing region: $REGION"

  # Get a list of all Lambda functions in the current region
  FUNCTIONS=$(aws lambda list-functions --region "$REGION" --query 'Functions[].FunctionName' --output json)

  # Check if there are any functions returned
  if [ -z "$FUNCTIONS" ] || [ "$FUNCTIONS" == "[]" ]; then
    echo "No Lambda functions found in $REGION."
    continue
  fi

  # Convert JSON array to Bash array
  readarray -t FUNCTION_NAMES <<< $(echo $FUNCTIONS | jq -r '.[]')

  # Loop over all function names and update the runtime management configuration
  for FUNCTION_NAME in "${FUNCTION_NAMES[@]}"
  do
    echo "Updating runtime management configuration for $FUNCTION_NAME in $REGION..."
    aws lambda put-runtime-management-config \
      --function-name "$FUNCTION_NAME" \
      --update-runtime-on "Auto" \
      --region "$REGION"
    echo "Updated $FUNCTION_NAME in $REGION"
  done
done

echo "All applicable functions across all specified regions have been updated."
