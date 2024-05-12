def get_errors_as_string(serializer):
    """
    Get the validation errors from a serializer as a string.
    """
    return "\n".join(
        [el.title() for values in serializer.errors.values() for el in values]
    )
