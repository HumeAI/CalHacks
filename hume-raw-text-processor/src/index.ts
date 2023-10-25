const BASE_URL = 'https://api.hume.ai/v0/batch/jobs';

// 1. Set your API Key
const HUME_API_KEY = '<your-api-key>';

// 2. Specify which Language
const language: Language = 'en';

// 3. Specify Language Model configuration
const languageModelConfig: LanguageModelConfig = {};

// 4. Copy and paste the text you'd like processed here
const rawTextInput = '';

// 5. Run `npm run start` to get inference results (predictions) from Hume's Language Model for the rawTextInput.
processRawText(rawTextInput, language, languageModelConfig).catch(
  (error: Error) => console.error('An error occurred:', error)
);

/**
 * Function which starts a job, polls the status of the job until status is `COMPLETED`, and then fetches the
 * job predictions.
 */
async function processRawText(
  rawText: string,
  language: Language,
  languageModelConfig: LanguageModelConfig
): Promise<void> {
  const MAX_RETRIES = 5; // adjust the number of retries here
  const INITIAL_DELAY_MS = 1000; // starting with 1 second delay

  let delay = INITIAL_DELAY_MS;
  const jobId = await startJob(rawText, language, languageModelConfig);

  // poll with exponential backoff
  for (let attempt = 0; attempt < MAX_RETRIES; attempt++) {
    const status = await getJobStatus(jobId);

    if (status === 'COMPLETED') {
      console.log('Status is COMPLETED!');
      const predictions = await getPredictions(jobId);
      console.log(JSON.stringify(predictions));
      return;
    }
    console.log(`Status is ${status}. Retrying in ${delay / 1000} seconds...`);
    await sleep(delay);
    delay *= 2; // exponential backoff
  }

  console.error('Max retries reached. Giving up.');
}

/**
 * See API Reference for more information on the start job endpoint: https://dev.hume.ai/reference/start_job
 */
async function startJob(
  rawText: string,
  language: Language,
  languageModelConfig: LanguageModelConfig
): Promise<string> {
  const body = JSON.stringify({
    text: [rawText],
    models: { language: languageModelConfig },
    transcription: { language },
  });
  const options = { ...buildHumeRequestOptions('POST'), body };
  const response = await fetch(BASE_URL, options);
  if (!response.ok) {
    throw new Error(`Failed to start job: ${response.statusText}`);
  }
  const json = await response.json();

  return json.job_id as string;
}

/**
 * See API Reference for more information on the get job details endpoint: https://dev.hume.ai/reference/get_job.
 */
async function getJobStatus(jobId: string): Promise<string> {
  const options = buildHumeRequestOptions('GET');
  const response = await fetch(`${BASE_URL}/${jobId}`, options);
  if (!response.ok) {
    throw new Error(`Failed to fetch job status: ${response.statusText}`);
  }
  const json = await response.json();

  return json.state.status;
}

/**
 * See API Reference for more information on the get job predictions endpoint: https://dev.hume.ai/reference/get_job_predictions.
 */
async function getPredictions(jobId: string): Promise<any> {
  const options = buildHumeRequestOptions('GET');
  const response = await fetch(`${BASE_URL}/${jobId}/predictions`, options);
  if (!response.ok) {
    throw new Error(`Failed to fetch job predictions: ${response.statusText}`);
  }
  const json = await response.json();

  return json;
}

/**
 * Helper function for building headers and options for Hume API requests.
 */
function buildHumeRequestOptions(method: 'GET' | 'POST'): {
  method: 'GET' | 'POST';
  headers: Headers;
} {
  const headers = new Headers();
  headers.append('X-Hume-Api-Key', HUME_API_KEY);
  headers.append('Content-Type', 'application/json');

  return { method, headers };
}

/**
 * Helper function to support exponential backoff implementation when polling for job status.
 */
function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/**
 * Language (ISO 639-1) Codes used to specify which language is to be processed. See our documentation
 * for supported languages here: https://dev.hume.ai/docs/supported-languages.
 */
type Language =
  | 'zh' // Chinese
  | 'da' // Danish
  | 'nl' // Dutch
  | 'en' // English
  | 'en-AU' // English (Australia)
  | 'en-IN' // English (India)
  | 'en-NZ' // English (New Zealand)
  | 'en-GB' // English (United Kingdom)
  | 'fr' // French
  | 'fr-CA' // French (Canadian)
  | 'de' // German
  | 'hi' // Hindi
  | 'hi-Latn' // Hindi (Roman Script)
  | 'id' // Indonesian
  | 'it' // Italian
  | 'ja' // Japanese
  | 'ko' // Korean
  | 'no' // Norwegian
  | 'pl' // Polish
  | 'pt' // Portuguese
  | 'pt-BR' // Portuguese (Brazil)
  | 'pt-PT' // Portuguese (Portugal)
  | 'ru' // Russian
  | 'es' // Spanish
  | 'es-419' // Spanish (Latin America)
  | 'sv' // Swedish
  | 'ta' // Tamil
  | 'tr' // Turkish
  | 'uk'; // Ukrainian

/**
 * The granularity at which to generate predictions. `utterance` corresponds to a natural pause or break in conversation, while
 * `conversational_turn` corresponds to a change in speaker. Granularity will default to `word` if not provided.
 */
type LanguageGranularity =
  | 'word'
  | 'sentence'
  | 'utterance'
  | 'conversational_turn';

/**
 * Configuration object which informs how Hume's Language model will process the text, and whether to include predictions from
 * the Sentiment and Toxicity models. See the start job endpoint for more details on job configuration:
 * https://dev.hume.ai/reference/start_job.
 */
type LanguageModelConfig = {
  granularity?: LanguageGranularity;
  sentiment?: {};
  toxicity?: {};
};
