@tool
def get_documentation(query: str) -> str:
    """
    Search the team's Word documents for information relevant to a question.

    Short documents are searched as complete files.
    Longer documents are split into smaller sections.

    Args:
        query: The topic or question to search for.
    """
    documents = read_all_word_documents(str(DOCUMENT_FOLDER))

    if not documents:
        return "No Word documents were found in the documentation folder."

    if not query.strip():
        return "A search question is required."

    ranked_results: list[dict] = []

    for document in documents:
        file_name = document["file_name"]
        content = document["content"]

        # Keep short documents whole.
        if len(content) <= 1000:
            sections = [content]

        # Split longer documents.
        else:
            sections = split_into_sections(content)

        for section_number, section_content in enumerate(sections, start=1):
            score = count_query_matches(
                query=query,
                text=section_content,
            )

            if score > 0:
                ranked_results.append(
                    {
                        "file_name": file_name,
                        "section_number": section_number,
                        "content": section_content,
                        "score": score,
                        "is_full_document": len(sections) == 1,
                    }
                )

    ranked_results.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    if not ranked_results:
        return "No relevant information was found in the documentation."

    selected_results: list[dict] = []
    results_per_file: dict[str, int] = {}

    for result in ranked_results:
        file_name = result["file_name"]
        current_count = results_per_file.get(file_name, 0)

        # Prevent one long document from taking every result.
        if current_count >= 2:
            continue

        selected_results.append(result)
        results_per_file[file_name] = current_count + 1

        if len(selected_results) >= 5:
            break

    formatted_results: list[str] = []

    for result in selected_results:
        file_name = result["file_name"]
        content = result["content"]

        if result["is_full_document"]:
            source_header = f"Source: {file_name}"
        else:
            section_number = result["section_number"]
            source_header = (
                f"Source: {file_name}\n"
                f"Section: {section_number}"
            )

        formatted_results.append(
            f"{source_header}\n"
            f"{content}"
        )

    return "\n\n---\n\n".join(formatted_results)
