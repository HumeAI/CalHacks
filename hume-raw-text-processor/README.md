# Hume Raw Text Processor

## Summary

This project serves as an example implementation of our Batch API processing raw text.

## Running Locally

1. Clone the repo with `git clone origin https://github.com/HumeAI/CalHacks.git`

2. Navigate to project directory `cd hume-raw-text-processor`

3. Install dependencies with `npm i`

4. Set configurations within the `src/index.ts` file.

   a. Input API Key.

   b. Specify which language.

   c. Set Language Model configurations.

   d. Copy paste the text to be processed.

5. Run `npm run start` to process the specified text with the specified configurations and get inference results.

## Notes

- The logic for fetching results utilizes polling with exponential backoff to wait for the job to complete before fetching the predictions. The maximum number of retries is set to `5`.
