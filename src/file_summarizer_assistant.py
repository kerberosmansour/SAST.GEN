from dotenv import load_dotenv
import os
from openai import OpenAI, AssistantEventHandler
from typing_extensions import override
from typing import List, Optional

# Load .env file
load_dotenv('.env')

# Now you can access the variables using os.getenv
api_key = os.getenv("OPENAI_API_KEY")

class FileSummarizerAssistant:
    """A class to interact with OpenAI's Assistant API for file summarization tasks."""

    def __init__(self, api_key: Optional[str] = None):
        """Initializes the FileSummarizerAssistant with OpenAI API key.

        Args:
            api_key (Optional[str]): The OpenAI API key. If not provided, will use the environment variable `OPENAI_API_KEY`.
        """
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.assistant = self._create_assistant()
        self.vector_store = self._create_vector_store()

    def _create_assistant(self):
        """Creates an assistant instance with file search capability.

        Returns:
            dict: The created assistant instance.
        """
        return self.client.beta.assistants.create(
            name="File Summarizer Assistant",
            instructions="You are a summarization assistant. Summarize the content of the files provided to you.",
            model="gpt-4o",
            tools=[{"type": "file_search"}],
        )

    def _create_vector_store(self):
        """Creates a vector store to store file embeddings.

        Returns:
            dict: The created vector store.
        """
        return self.client.beta.vector_stores.create(name="File Summarizer Store")

    def _upload_files(self, file_paths: List[str]):
        """Uploads files to the vector store.

        Args:
            file_paths (List[str]): List of file paths to be uploaded.

        Returns:
            dict: The file batch information after upload.

        Raises:
            Exception: If the file upload fails.
        """
        file_streams = [open(file_path, "rb") for file_path in file_paths]
        file_batch = self.client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=self.vector_store.id, files=file_streams
        )

        # Ensure all streams are closed
        for stream in file_streams:
            stream.close()

        if file_batch.status != "completed":
            raise Exception(f"File upload failed: {file_batch.status}")
        
        return file_batch

    def summarize_files(self, file_paths: List[str], question: str) -> str:
        """Summarizes the content of the provided files based on the given question.

        Args:
            file_paths (List[str]): List of file paths to be summarized.
            question (str): The question or prompt to guide the summarization.

        Returns:
            str: The summarized text output.
        """
        self.assistant = self.client.beta.assistants.update(
            assistant_id=self.assistant.id,
            tool_resources={"file_search": {"vector_store_ids": [self.vector_store.id]}},
        )

        # Upload the files
        self._upload_files(file_paths)
        message_file = self.client.files.create(
            file=open(file_paths[0], "rb"), purpose="assistants"
        )

        # Create a thread and attach the files
        thread = self.client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": question,
                    "attachments": [
                        {"file_id": message_file.id, "tools": [{"type": "file_search"}]}
                    ],
                }
            ]
        )

        return self._stream_answer(thread.id)

    def _stream_answer(self, thread_id: str) -> str:
        """Streams the assistant's answer to the provided thread.

        Args:
            thread_id (str): The thread ID to stream the answer from.

        Returns:
            str: The value field of the final text output.
        """
        class EventHandler(AssistantEventHandler):
            def __init__(self):
                super().__init__()
                self.result = ""

            @override
            def on_text_created(self, text) -> None:
                # Directly access the value field if it's a Text object
                if hasattr(text, 'value'):
                    self.result += text.value

            @override
            def on_message_done(self, message) -> None:
                # Ensure to extract just the text content
                if hasattr(message.content[0], 'text') and hasattr(message.content[0].text, 'value'):
                    self.result += message.content[0].text.value

        event_handler = EventHandler()

        with self.client.beta.threads.runs.stream(
            thread_id=thread_id,
            assistant_id=self.assistant.id,
            event_handler=event_handler,
            instructions="Please read leverage the knowledge base in the files attached, and answer the application security questions as detailed and as acurate as possible. The user is an application security engineers and they need an answer that has limited false positive and false negatives as possible.",
        ) as stream:
            stream.until_done()

        return event_handler.result

    def cleanup(self) -> None:
        """Cleans up resources by deleting files and the vector store."""
        file_ids = [
            file.id for file in self.client.beta.vector_stores.files.list(vector_store_id=self.vector_store.id)
        ]
        for file_id in file_ids:
            self.client.beta.vector_stores.files.delete(vector_store_id=self.vector_store.id, file_id=file_id)
        self.client.beta.vector_stores.delete(vector_store_id=self.vector_store.id)

if __name__ == "__main__":
    api_key = os.getenv("OPENAI_API_KEY")
    file_summarizer = FileSummarizerAssistant(api_key=api_key)
    try:
        file_paths = ["/Users/sherif/Documents/GitHub/Investigator/Testing/letter.pdf"]
        question = "Please summarize the key points from these documents, do not use markdown just respond in plain text."
        answer = file_summarizer.summarize_files(file_paths, question)
        print("\nSummary:\n", answer, "\nType of answer: ", type(answer))
    finally:
        file_summarizer.cleanup()