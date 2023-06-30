from dataclasses import asdict
from typing import Optional, List, Mapping, Any

from llama_cpp import Llama
from langchain.llms.base import LLM

from llm_data import llm_data

class haiiLLM(LLM):
    model_path: str
    llm: Llama
    params: Mapping[str, Any]
    
    @property
    def _llm_type(self) -> str:
        return "haii-llm"

    def __init__(self, model_path: str, data: llm_data, **kwargs: Any):
        model_path = model_path
        llm = Llama(model_path=model_path)
        params = asdict(data)
        super().__init__(model_path=model_path, llm=llm, params=params, **kwargs)

    def update_params(self, data: llm_data):
        self.params = asdict(data)

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        response = self.llm(prompt,
                            suffix=None,
                            max_tokens=self.params["max_tokens"],
                            temperature=self.params["temperature"],
                            top_p=self.params["top_p"],
                            echo=False,
                            frequency_penalty=self.params["frequency_penalty"],
                            presence_penalty=self.params["presence_penalty"],
                            repeat_penalty=self.params["repeat_penalty"],
                            top_k=self.params["top_k"],
                            stop=stop or self.params["stop"])
        return response["choices"][0]["text"]

    async def _acall(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        response = self.llm(prompt,
                            suffix=None,
                            max_tokens=self.params["max_tokens"],
                            temperature=self.params["temperature"],
                            top_p=self.params["top_p"],
                            echo=False,
                            frequency_penalty=self.params["frequency_penalty"],
                            presence_penalty=self.params["presence_penalty"],
                            repeat_penalty=self.params["repeat_penalty"],
                            top_k=self.params["top_k"],
                            stop=stop or self.params["stop"])
        return response["choices"][0]["text"]

    @property
    def model_params(self) -> Mapping[str, Any]:
        return self.__getstate__()["__dict__"]["llm"].__getstate__()
    
    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {"model_path": self.model_path}

    @property
    def llm_params(self) -> Mapping[str, Any]:
        return {"context": self.params["context"],
                "max_tokens": self.params["max_tokens"],
                "temperature": self.params["temperature"],
                "top_p": self.params["top_p"],
                "frequency_penalty": self.params["frequency_penalty"],
                "presence_penalty": self.params["presence_penalty"],
                "repeat_penalty": self.params["repeat_penalty"],
                "top_k": self.params["top_k"],
                "stop": self.params["stop"]}
