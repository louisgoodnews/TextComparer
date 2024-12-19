import spacy

from typing import *

from logger.logger import Logger


class TextComparer:
    """
    A singleton class for comparing text similarity using spaCy language models.

    This class provides functionality to load language models and compare text similarities
    using spaCy's natural language processing capabilities. It implements the singleton
    pattern to ensure efficient resource usage and maintains a cache of loaded language
    models to improve performance.

    Attributes:
        _shared_instance (Self | None): Singleton instance of the class
        _language_models (Dict[str, spacy.Language]): Cache of loaded spaCy language models
    """

    _shared_instance: Self | None = None
    _language_models: Dict[str, spacy.Language] = {}

    def __new__(cls) -> Self:
        """
        Create or return the singleton instance of TextComparer.

        Returns:
            Self: The singleton instance of TextComparer
        """
        if cls._shared_instance is None:
            cls._shared_instance = super().__new__(cls)
            cls._shared_instance.init()
        return cls._shared_instance

    def init(self) -> None:
        """
        Initialize the TextComparer instance.

        Sets up logging and initializes internal state variables.
        """
        self.logger = Logger.get_logger(name=self.__class__.__name__)
        self.logger.info(message=f"Initialized {self.__class__.__name__}...")

        self._language: str = ""
        self._nlp: spacy.Language | None = None

    @property
    def language(self) -> str:
        """
        Get the currently loaded language model name.

        Returns:
            str: The name of the currently loaded language model
        """
        return self._language

    @language.setter
    def language(self, value: str) -> None:
        """
        Set the language model name.

        Args:
            value (str): The name of the language model to use

        Raises:
            ValueError: If the provided language name is empty
        """
        if not value:
            raise ValueError("Language cannot be empty")
        self._language = value

    async def load_language(
        self,
        language: str,
    ) -> None:
        """
        Asynchronously load a spaCy language model.

        This method loads the specified language model if it's not already loaded.
        Previously loaded models are cached to improve performance.

        Args:
            language (str): The name of the spaCy language model to load (e.g., 'en_core_web_sm')

        Raises:
            ValueError: If the language model name is empty
            RuntimeError: If the language model fails to load
            Exception: For other unexpected errors during model loading
        """
        if not language:
            raise ValueError("Language model name cannot be empty")

        try:
            # Check if model is already loaded
            if language in self._language_models:
                self._nlp = self._language_models[language]
                self._language = language
                return

            # Load new model
            self._nlp = spacy.load(language)
            self._language_models[language] = self._nlp
            self._language = language

            self.logger.info(f"Successfully loaded language model '{language}'")
        except OSError as e:
            raise RuntimeError(
                f"Failed to load language model '{language}'. Make sure it's installed: {e}"
            )
        except Exception as e:
            self.logger.error(
                message=f"Caught an exception while attempting to load language '{language}': {e}"
            )
            raise

    async def compare_similarity(
        self,
        source: str,
        target: str,
        language: str | None = None,
    ) -> float:
        """
        Compare two texts and return their similarity score.

        This method processes the input texts using spaCy and calculates their similarity
        using the loaded language model. If a different language model is specified, it
        will be loaded automatically.

        Args:
            source (str): The source text to compare
            target (str): The target text to compare against
            language (str | None): Optional language model to use. If not provided, uses current model

        Returns:
            float: Similarity score between 0 and 1, where 1 indicates identical meaning
                  and 0 indicates completely different meaning

        Raises:
            ValueError: If texts are empty or language model is not loaded
            RuntimeError: If no language model is loaded
            Exception: For other unexpected errors during comparison
        """
        if not source or not target:
            raise ValueError("Source and target texts cannot be empty")

        try:
            # Load language if needed
            if language and self._language != language:
                await self.load_language(language=language)

            if not self._nlp:
                raise RuntimeError(
                    "No language model loaded. Call load_language first."
                )

            # Process texts
            doc1: spacy.tokens.doc.Doc = self._nlp(source)
            doc2: spacy.tokens.doc.Doc = self._nlp(target)

            return doc1.similarity(doc2)
        except Exception as e:
            self.logger.error(
                message=f"Caught an exception while attempting to compare texts: {e}"
            )
            raise
