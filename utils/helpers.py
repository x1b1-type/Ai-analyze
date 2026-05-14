def read_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        return uploaded_file.read().decode("utf-8")
    return ""

def get_download_link(text: str):
    return text.encode('utf-8')