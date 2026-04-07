# !pip install llama-cpp-python

from llama_cpp import Llama

llm = Llama.from_pretrained(
	repo_id="EnlistedGhost/Anubis-Mini-11B-v1-Vision-OLLAMA",
	filename="Anubis-Mini-11B-v1-Vision-F16.gguf",
)

output = llm(
	"Once upon a time,",
	max_tokens=512,
	echo=True
)
print(output)