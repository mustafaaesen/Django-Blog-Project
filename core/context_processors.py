# core/context_processors.py

def global_context(request):
    """
    Tüm template'lerde (layout, navbar, footer, errors vs.)
    kullanılabilecek temel context verileri.
    """
    return {
        "user": getattr(request, "user", None),
        "request": request
    }
