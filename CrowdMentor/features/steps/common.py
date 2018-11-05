from behave import given, when, then
from test.factories.user import UserFactory
from .users.profile import Profile
from .users.UserRoles import UserRoles

# Home page is not correctly defined!
@then('I am redirected to the home page')
def step_impl(context):
    br=context.browser
    #br.visit(context.get_url())
    # Checks success status
    #print(br.url)
    #print(context.get_url())
    #print(dir(context))
    #print('after submit', br.url)
    #print('after submit', br.html)
    assert not br.url.endswith('next=/')

@given('I am an existing user who tries to access the site')
def step_impl(context):
    u = UserFactory(username='foo', email='foo@example.com')
    u.set_password('bar')
    # Don't omit to call save() to insert object in database
    u.save()

@given('I am an existing user with task updater access')
def step_impl(context):
    u = UserFactory(username='task_updater', email='tu@example.com')
    u.set_password('bar')
    u.save()
    p = Profile.objects.get(user_id=u.id)
    p.role = UserRoles.TASK_UPDATER.value
    p.save()

@given('I am an admin')
def step_impl(context):
    u = UserFactory(username='admin', email='theadmin@example.com')
    u.set_password('bar')
    u.save()
    p = Profile.objects.get(user_id=u.id)
    p.role = UserRoles.ADMIN.value
    p.save()

@given('there is one user with worker access')
def step_impl(context):
    u = UserFactory(username='foo', email='foo@example.com')
    u.set_password('bar')
    # Don't omit to call save() to insert object in database
    u.save()

@given('I am an user logged in as the user with task updater access')
def step_impl(context):
    br = context.browser
    br.visit(context.base_url)

    # Fill login form and submit it (valid version)
    br.fill('username', 'task_updater')
    br.fill('password', 'bar')
    br.find_by_id('submit').first.click()

@given('I am logged in as admin')
def step_impl(context):
    br = context.browser
    br.visit(context.base_url)

    # Fill login form and submit it (valid version)
    br.fill('username', 'admin')
    br.fill('password', 'bar')
    br.find_by_id('submit').first.click()
