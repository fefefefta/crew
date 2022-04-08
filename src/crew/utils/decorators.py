from django.shortcuts import redirect


def staff_only(view):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        if not request.user.is_staff:
            return Exception('u r not allowed to be here zhulic')

        return view(request, *args, **kwargs)

    return wrapper
