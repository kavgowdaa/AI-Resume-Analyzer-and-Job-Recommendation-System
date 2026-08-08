import re

def clean_text(text):
    """
    Clean resume text while preserving technical terms like
    C++, C#, and .NET.
    """

    # Convert to lowercase
    text = text.lower()

    # Preserve special technical terms
    text = text.replace("c++", "cplusplus")
    text = text.replace("c#", "csharp")
    text = text.replace(".net", "dotnet")

    # Remove punctuation except letters, numbers and spaces
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # Restore preserved terms
    text = text.replace("cplusplus", "c++")
    text = text.replace("csharp", "c#")
    text = text.replace("dotnet", ".net")

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text