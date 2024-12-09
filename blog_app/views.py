from django.shortcuts import render
import requests
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.shortcuts import render, redirect
from datetime import datetime
from django.utils import timezone
from .forms import PostForm, CreateUserForm, LoginForm, CreateCommentForm

# Create your views here.

def index(request):
    # Check if 'username' exists in the session
    username = request.session.get('username')  # Use .get() to avoid KeyError
    print('USERNAME IS', username)

    api_url_all_posts = 'https://blogapplications.pythonanywhere.com/create/'  # API to fetch all posts
    user_specific_api_url = f'https://blogapplications.pythonanywhere.com/usersearch/{username}'  # API to fetch user-specific data
    comment_url = f'https://blogapplications.pythonanywhere.com/api/comment-count/'

    try:
        # Fetch all posts
        response_all = requests.get(api_url_all_posts)
        if response_all.status_code == 404:
            print(f"Error: All posts not found - status code {response_all.status_code}")
            all_posts = None
        else:
            all_posts = response_all.json()

        comment_all = requests.get(comment_url)
        if comment_all.status_code == 404:
            print(f"Error: Comment count not found - status code {comment_all.status_code}")
            comment_total = None
        else:
            comment_total = comment_all.json()

        # Initialize variables
        user_data = None
        posted = None  # Initialize posted to avoid UnboundLocalError

        # Fetch user-specific data if 'username' exists
        if username:
            response_user = requests.get(user_specific_api_url)
            if response_user.status_code == 200:
                user_data = response_user.json()
                print('USERDATA IS', user_data)
            elif response_user.status_code == 404:
                print(f"Error: User-specific data not found for username {username} - status code {response_user.status_code}")

        # Handle pagination for all posts
        if all_posts:  # Ensure all_posts is not None
            paginator = Paginator(all_posts, 2)
            try:
                page = int(request.GET.get('page', 1))
            except ValueError:
                page = 1
            try:
                posted = paginator.page(page)
            except (EmptyPage, InvalidPage):
                posted = paginator.page(paginator.num_pages)

        # Render template with both all posts and user-specific posts
        context = {
            'posted': posted,
            'user_data': user_data,
            'username': username,
            'comment_all': comment_total,
        }
        return render(request, 'index.html', context)

    except Exception as e:
        print(f"Error: {e}")
        return render(request, 'index.html', {'error': str(e)})



    
    


def create_user(request):

    if request.method == 'POST':
        form = CreateUserForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                # Save the form data to the database (optional)
                form.save()
                image  = request.FILES['profile_picture']
                image.seek(0)

                # Send the form data to the REST API
                api_url = 'https://blogapplications.pythonanywhere.com/users/'
                data = form.cleaned_data
                print("Data to be sent:", data)  # Debug: Check data format
                files = {'profile_picture': (image.name, image.read(), image.content_type)}
                print(files)
                response = requests.post(api_url, data=data, files=files)
                print(response.status_code)
                # Handle the API response
                if response.status_code == 201:
                    messages.success(request, 'User Registerd Successfully!')
                    return redirect(f'/user_logins')  # Replace 'success_page' with your actual success page
                else:
                    messages.error(request, f'Error submitting data to the REST API: {response.status_code}')
                    print("API Error Response:", response.json())  # Debug: Check API error response
            except requests.RequestException as e:
                messages.error(request, f'Error during API request: {str(e)}')
        else:
            messages.error(request, 'Form is not valid. Please check the input.')
            print('Form errors:', form.errors)
    else:
        form = CreateUserForm()


    return render(request, 'register.html', {'form': form})

    


def user_logins(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Extract username and password from the form
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print('USERNAME IS',username)

            # Send login data to the API
            api_url = 'https://blogapplications.pythonanywhere.com/user_login/'
            api_data = {
                'username': username,
                'password': password,
            }
            print(api_data)

            response = requests.post(api_url, json=api_data)
            print(response.status_code  )

            if response.status_code == 200:  # Assuming a successful login status code
                request.session['username']=username
                
                # You may want to save the user session or token for subsequent requests
                messages.success(request, f'{username} logged in successfully')
                return redirect('/')  # Redirect to the dashboard or another success page
            else:
                # Handle API error and display error message
                api_error = response.json().get('error', 'Unknown API error')
                messages.error(request, f'API Error: {api_error}')
        else:
            # Handle form validation errors
            messages.error(request, 'Form validation failed. Please check the entered data.')

    return render(request, 'login.html')
def user_logout(request):
    # Remove the username from the session
    if 'username' in request.session:
        del request.session['username']
    
    # Redirect to the login page or homepage
    return redirect('/')


def post_fetch(request, id):
    username = request.session.get('username')  # Use .get() to avoid KeyError
    
    user_specific_api_url = f'https://blogapplications.pythonanywhere.com/usersearch/{username}'  # API to fetch user-specific data

    try:
        # Initialize user-specific data as None
        user_data = None
        
        # Fetch user-specific data if 'username' exists
        if username:
            response_user = requests.get(user_specific_api_url)
            print(response_user)
            if response_user.status_code == 200:
                user_data = response_user.json()
                print('USERDATA IS',user_data)
    except requests.RequestException as e:
        
        user_data = None
    # username = request.session.get('username')  # Use .get() to avoid KeyError
    # Fetch details of the specific post by id
    api_url = f'https://blogapplications.pythonanywhere.com/post_detail/{id}'  # Replace with your API endpoint for a single post
    
    
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            post_data = response.json()  # Assuming the API returns JSON data
            
        else:
            
            post_data = None  # In case of an error, set post_data to None
    except requests.RequestException as e:
        
        post_data = None

    # Fetch details of the specific post by id
    comment_url = f'https://blogapplications.pythonanywhere.com/post_by_search/{id}'  # Replace with your API endpoint for a single post
    
    
    try:
        response = requests.get(comment_url)
        if response.status_code == 200:
            comment_data = response.json()  # Assuming the API returns JSON data
            
        else:
            
            comment_data = None  # In case of an error, set post_data to None
    except requests.RequestException as e:
        print(f"Error with API request for specific post: {e}")
        comment_data = None    

    # Fetch all posts (even if fetching the specific post fails)
    api_urls = 'https://blogapplications.pythonanywhere.com/create/'  # Replace with your API endpoint for all posts
    
    
    try:
        response = requests.get(api_urls)
        if response.status_code == 200:
            all_posts_data = response.json()  # Assuming the API returns JSON data
            
        else:
            
            all_posts_data = None  # Set to None in case of error
    except requests.RequestException as e:
        
        all_posts_data = None

    
    # Render the page with both the post data and all posts data
    return render(request, 'detail_page.html', {
        'post': post_data,
        'all_post': all_posts_data,
        'comment_data':comment_data,
        'username':username,
        'user_data':user_data,
        'error_message': None if post_data or all_posts_data else 'There was an error fetching data.'
    })

def delete_post(request, post_id):
    print('Delete Here', post_id)
    api_url = f'https://blogapplications.pythonanywhere.com/post/{post_id}/delete/'  # Replace with your actual API URL

    response = requests.delete(api_url)

    if response.status_code == 204:
        messages.success(request, f"Post with ID {post_id} has been deleted.")
    else:
        messages.error(request, f"Post with ID {post_id} has not been deleted.")
    return redirect('/')

def comment_create(request):
    username = request.session.get('username')  # Use .get() to avoid KeyError
    print('USERNAME IS', username)
    if request.method == 'POST':
        post_id = request.POST.get('post')
        form = CreateCommentForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                # Save the form data to the database (optional)
                form.save()

                # Send the form data to the REST API
                api_url = 'https://blogapplications.pythonanywhere.com/create_comment/'
                data = form.cleaned_data
                print("Data to be sent:", data)  # Debug: Check data format

                response = requests.post(api_url, data=data)

                # Handle the API response
                if response.status_code == 201:
                    messages.success(request, 'Comment added successfully!')
                    return redirect(f'/post_fetch/{post_id}')  # Replace 'success_page' with your actual success page
                else:
                    messages.error(request, f'Error submitting data to the REST API: {response.status_code}')
                    print("API Error Response:", response.json())  # Debug: Check API error response
            except requests.RequestException as e:
                messages.error(request, f'Error during API request: {str(e)}')
        else:
            messages.error(request, 'Form is not valid. Please check the input.')
            print('Form errors:', form.errors)
    else:
        form = CreateCommentForm()

    return render(request, 'detail_page.html', {'form': form})


 
def dashboard(request, id):
    current_time = timezone.localdate()
    print(current_time)

    all_post_added = None

    count_url = f'https://blogapplications.pythonanywhere.com/comment_count/{1}/{id}/'  # Replace with your API endpoint for a single post
    
    
    
    try:
        response = requests.get(count_url)

        if response.status_code == 200:
            count_data = response.json()  # Assuming the API returns JSON data
            
        else:
            
            count_data = None  # In case of an error, set post_data to None
    except requests.RequestException as e:
        print(f"Error with API request for specific post: {e}")
        user_data = None 

    comment_url = f'https://blogapplications.pythonanywhere.com/api/comment-count/'

    try:
        comment_status = requests.get(comment_url)

        if comment_status.status_code == 200:
            comment_total = comment_status.json()   # Assuming the API returns JSON data
            
        else:
            
            comment_total = None  # In case of an error, set post_data to None
    except requests.RequestException as e:
        print(f"Error with API request for specific post: {e}")
        comment_total = None    

    

           


    # Fetch details of the specific post by id
    comment_url = f'https://blogapplications.pythonanywhere.com/user_by_search/{id}/'  # Replace with your API endpoint for a single post
    
    
    try:
        response = requests.get(comment_url)
        if response.status_code == 200:
            user_data = response.json()  # Assuming the API returns JSON data
            
        else:
            
            user_data = None  # In case of an error, set post_data to None
    except requests.RequestException as e:
        print(f"Error with API request for specific post: {e}")
        user_data = None 


    # Fetch details of the specific post by id
    user_post_url = f'https://blogapplications.pythonanywhere.com/user_by_post/{id}/'  # Replace with your API endpoint for a single post
    
    
    try:
        response = requests.get(user_post_url)
        if response.status_code == 200:
            user_post = response.json()  # Assuming the API returns JSON data
            
        else:
            
            user_post = None  # In case of an error, set post_data to None
    except requests.RequestException as e:
        print(f"Error with API request for specific post: {e}")
        user_post = None


    if user_post:  # Ensure all_posts is not None
            paginator = Paginator(user_post, 3)
            try:
                page = int(request.GET.get('page', 1))
            except ValueError:
                page = 1
            try:
                all_post_added = paginator.page(page)
            except (EmptyPage, InvalidPage):
                all_post_added = paginator.page(paginator.num_pages)



    return render(request,'dashboard.html', {'user_data': user_data, 'user_post':all_post_added, 'current_time':current_time, 'count_data':count_data, 'comment_total':comment_total})



#Post blog Section  





def post_create(request, id):
    print('Author Id', id)
    username = request.session.get('username')  # Use .get() to avoid KeyError
    print('USERNAME IS', username)
    if request.method == 'POST':
        post_id = request.POST.get('post')
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                # Save the form data to the database (optional)
                form.save()
                image  = request.FILES['blog_image']
                image.seek(0)

                # Send the form data to the REST API
                api_url = 'https://blogapplications.pythonanywhere.com/create/'
                data = form.cleaned_data

                files = {'blog_image': (image.name, image.read(), image.content_type)}
                response = requests.post(api_url, data=data, files=files)

                # Handle the API response
                if response.status_code == 201:
                    messages.success(request, 'Post added successfully!')
                    return redirect(f'/dashboard/{id}/')  # Replace 'success_page' with your actual success page
                else:
                    messages.error(request, f'Error submitting data to the REST API: {response.status_code}')
                    print("API Error Response:", response.json())  # Debug: Check API error response
            except requests.RequestException as e:
                messages.error(request, f'Error during API request: {str(e)}')
        else:
            messages.error(request, 'Form is not valid. Please check the input.')
            print('Form errors:', form.errors)
    else:
        form = PostForm()

    return render(request, 'detail_page.html')    




def update_post(request, id, user_id): 
    print('Passing id is', id)
    if request.method == 'POST':
        # name = request.POST['Name']
        # Prep_time = request.POST['Prep_time'] 
        # Difficulty = request.POST['Difficulty']
        # recipe_img = request.POST['recipe_img']
        # Vegetarian = request.POST.get('Vegetarian', 'false')
        # if request.POST['Vegetarian'] == 'true':
        #     Vegetarian = True
        # else:
        #     Vegetarian = False
            

        # print('Image Url', recipe_img)
        # description = request.POST['description']

        api_url = f'https://blogapplications.pythonanywhere.com/post_update/{id}/'  # Make sure to include a trailing slash
        data = {
                    'post_name': request.POST['post_name'],
                    'post_slug': request.POST['post_slug'], 
                    'blog_preview': request.POST['blog_preview'], 
                    'blog_content': request.POST['blog_content'],   
                    'blog_image': request.POST['blog_image'], 
                    'category':request.POST['category'], 
                    'Status': request.POST['Status'], 
                    'visibility': request.POST['visibility'], 
                    'Comments': request.POST['Comments'], 
                    'updated_by': request.POST['updated_by'], 
                    'author_name': request.POST['author_name'], 
                    'author_id': request.POST['author_id'], 


                    }
        print('Updated Data', data)
            
        response = requests.put(api_url, data=data)  # Assuming you want to use the PUT method
        print(response.status_code)
        if response.status_code == 200:
            messages.success(request, 'Post Updated Successfully!')
            print('Post Updated Successfully!')
            return redirect(f'/dashboard/{user_id}/')  # Replace 'success_page' with your actual success page
        else:
            messages.error(request, f'Error submitting data to the REST API: {response.status_code}')
        messages.success(request, 'Recipe Inserted Successfully!')
    
    
    return render(request, 'receipe_update.html')
