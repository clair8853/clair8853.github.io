import torch
from transformers import PegasusTokenizer, PegasusForConditionalGeneration

def download_model():
    try:
        print("Downloading tokenizer...")
        tokenizer = PegasusTokenizer.from_pretrained("google/pegasus-pubmed")
        print("Tokenizer downloaded successfully")
        
        print("\nDownloading model...")
        model = PegasusForConditionalGeneration.from_pretrained("google/pegasus-pubmed")
        print("Model downloaded successfully")
        
        if torch.cuda.is_available():
            print("\nMoving model to GPU...")
            model = model.to("cuda")
            print(f"Model moved to GPU: {torch.cuda.get_device_name(0)}")
            
        print("\nTesting model with sample text...")
        sample_text = "This is a test of the summarization model."
        inputs = tokenizer(sample_text, max_length=1024, truncation=True, return_tensors="pt")
        if torch.cuda.is_available():
            inputs = inputs.to("cuda")
        
        summary_ids = model.generate(inputs["input_ids"])
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        print(f"Sample summary: {summary}")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    download_model()
