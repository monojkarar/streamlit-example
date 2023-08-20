from google.cloud import aiplatform
import vertexai
from vertexai.language_models import TextGenerationModel


def init_vertex_ai():
    vertexai.init(project="team-11-lifesight-hack", location="us-central1")


def get_vertex_ai_model(model_name="text-bison@001"):
    return TextGenerationModel.from_pretrained(model_name)


def get_response_from_prompt(prompt="""My h1ac is 7 suggest me a diet plan"""):
    model = get_vertex_ai_model()
    parameters = {
        "max_output_tokens": 1024,
        "temperature": 0.2,
        "top_p": 0.8,
        "top_k": 40
    }
    response = model.predict(
        prompt,
        **parameters
    )

    return response


def print_response(response="_"):
    print(f"Response from Model: {response}")


def connect():
    aiplatform.init(
        # your Google Cloud Project ID or number
        # environment default used is not set
        project='team-11-lifesight-hack',

        # the Vertex AI region you will use
        # defaults to us-central1
        location='us-central1',

        # Google Cloud Storage bucket in same region as location
        # used to stage artifacts
        staging_bucket='gs://hackathon-swat-bucket',

        # custom google.auth.credentials.Credentials
        # environment default creds used if not set
        # credentials=my_credentials,

        # customer managed encryption key resource name
        # will be applied to all Vertex AI resources if set
        # encryption_spec_key_name=my_encryption_key_name,

        # the name of the experiment to use to track
        # logged metrics and parameters
        experiment='hackathon-swat-app',

        # description of the experiment above
        experiment_description='App to summarize your health report and suggest health plans'
    )
