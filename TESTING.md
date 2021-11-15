# perkulater - Testing #

## Contents ##
- [Automated Testing](#automated-testing)
    - [HTML](#html)
    - [Custom CSS Styling](#custom-css-styling)
    - [JavaScript Code Testing](#javascript-code-testing)
    - [Python Code Testing](#python-code-testing)
    - [Automated Performance And Quality Testing](#automated-performance-and-quality-testing)
- [User Stories Testing](#user-stories-testing)
- [Manual Testing](#manual-testing)
    - [Features](#form-validation)
    - [Form Validation](#form-validation)
    - [Responsive Design](#responsive-design)
    - [Browser Compatibility Testing](#browser-compatibility-testing)
- [Bugs Fixed During Testing](#bugs-fixed-during-testing)
- [Bugs Remaining](#bugs-remaining)

## Automated Testing ##

### HTML ###
All **HTML** code was validated using the [W3C Markup Validation Service](https://validator.w3.org/) 
regularly during the development process. **The HTML Source Code** was regularly viewed for each page 
using **Google Chrome** (right click, *View page source*) and passed through the 
[W3C Markup Validation Service](https://validator.w3.org/).  
Various minor errors were encountered and corrected during the final **HTML** validation check. 
All HTML code now passes validation with no errors or warnings. See [HTML Validation Reports](media/testing/validation/html)

### Custom CSS Styling ###
[Custom CSS styling](/static/css/style.css) was validated using the [W3C CSS Validation Service](https://jigsaw.w3.org/css-validator/).  
No errors were generated. Some "Due to their dynamic nature, CSS variables are currently not statically checked" 
warnings were generated. See [CSS Validation Reports](/static/testing/validation/css).  
These warnings are related to the global variables declared at the top of the [Custom Base CSS](/static/css/style.css). 
The warnings are generated because the [W3C CSS Validation Service](https://jigsaw.w3.org/css-validator/) 
does not currently support CSS global variable declaration and are not considered to be an issue. 
See [Github Link](https://github.com/w3c/css-validator/pull/173).
Some additional "vendor extension" warnings were also generated in **base.css**. These warnings are not considered to be an issue 
and the vendor extensions are to enable correct display of the **Background Image** linear gradient and various **Form** elements.  

### JavaScript Code Testing ##
The custom **base**, **basket**, **checkout**, **home**, **products**, and **profiles** **JavaScript Code Libraries** 
were validated using the [JSHint](https://jshint.com/about/) static code analysis tool, and passed without errors or warnings.
See [JavaScript Event Handler Module Validation](/static/testing/validation/js/events-jshint-validation.pdf). 
Due to the lack of complexity of **JavaScript** code implemented on the project, **Automated Unit Testing** 
of the **JavaScript** code was considered unecessary. All **JavaScript** functions and event handlers in the custom **JavaScript Code Libraries** 
have been thoroughly manually tested as part of the [Manual Testing](#manual-testing) process.  

### Python Code Testing ##
All **Python Code** was thoroughly de-bugged and tested at the command line during the development process, and has been validated 
using [Flake 8](https://pypi.org/project/flake8/). [flake8-django](https://pypi.org/project/flake8-django/) was installed to assist with validation.  
**Flake 8** was configured for **perkulater** by creating a `setup.cfg` file in the root of the project, which contains the following settings:
```
[flake8]
exclude = */migrations/*.py, *__init__.py, *_pychache_*
per-file-ignores = *apps.py:F401, *settings.py:E501
```
The settings exclude **django** migrations, `__init__.py`, and `_pychache_` files, as these are system generated files and do not need to be checked.  
*F401* (imported but unused) errors are ignored for *apps.py, as flake8 was throwing an error on **Django** signals being imported but unused. 
Signals need to be imported into the **app** config files to ensure correct operation of the code.  
*E501* (line too long) errors are ignored for `settings.py` as it is not possible to shorten these lines of code without causing application errors.  

**Flake 8** output is shown here [Python Code Automated Testing And Flake8 Output](/static/testing/validation/python/python-automated-testing-output.png).

Python **Automated Unit Testing** was also implemented using the [Django Unit Testing](https://docs.djangoproject.com/en/3.2/topics/testing/overview/) framework.  
. **Unit Tests** have been written for all **Forms**, **Model Methods**, **Signals** and **Views**, for each **Django App** in  the **perkulater** project. 
A total of **137** **Unit Tests** have been written. Once **Unit Testing** was implemented, **Unit Tests** were run each time a feature was added or changed.  
All **137** tests run successfully without errors or warnings, see [Python Code Automated Testing And Flake8 Output](/static/testing/validation/python/python-automated-testing-output.png).  

### Automated Performance And Quality Testing ###
Performance and Quality was tested with the [Lighthouse](https://chrome.google.com/webstore/detail/lighthouse/blipmdconlkpinefehnmjammfjpmpbjk?hl=en) 
extension for [Google Chrome](https://www.google.com/intl/en_uk/chrome/). 

Initial [Lighthouse](https://chrome.google.com/webstore/detail/lighthouse/blipmdconlkpinefehnmjammfjpmpbjk?hl=en) scores were:
* **Performance** 84%
* **Accessibility** 90%
* **Best Practices** 93%
* **SEO** 94%  

See [Initial Lighthouse Report](/static/testing/validation/performance/lighthouse-report-1.pdf).

To improve **Accesibility**, the *name* and *aria-label* atttributes were added to the **Search** and **Add** 
buttons as required on the **Home** page.

To improve **Best Practices** and **Performance**, the [FreeFrom logo](/static/testing/logo.png) was re-sized to 
94px x 100px and compressed using the [GIMP](https://www.gimp.org/) and [RIOT](https://riot-optimizer.com/) 
image manipulation and optimisation tools and the *defer* attribute was added to the script HTML tags, 
to defer loading of the **JavaScript** files.

Final [Lighthouse](https://chrome.google.com/webstore/detail/lighthouse/blipmdconlkpinefehnmjammfjpmpbjk?hl=en) scores were:
* **Performance** 86%
* **Accessibility** 98%
* **Best Practices** 100%
* **SEO** 94%  

See [Final Lighthouse Report](/static/testing/validation/performance/lighthouse-report-2.pdf).

Note that the slightly lower performance score of 86% is due to render blocking resources (mainly from **Bootstrap**) and 
unused CSS (also from **Bootstrap**). To improve performance, consideration should be given in a **Future Development Phase** 
to optimising **Bootstrap** and **DataTables** by only importing the required components. 
See this [Link](https://getbootstrap.com/docs/5.0/customize/optimize/) for further information.

## User Stories Testing ###
* ***As a User, I would like to be able to register on the site.***  
The user is able to **Register** on the site using the **Register** form, which can be accessed from **Home Page Alert Links** 
or from the **Sign In** form. Once the **Register** form has been populated and the [Form Validation](#form-validation) and checking has been 
passed, the user is registered on the database, redirected back to the **Home** page, and notified with a message 
at the top of the screen. The **Home Page Alert** is updated to remove the **Sign In** and **Register** links and shows the 
**User Name** of the signed in user. The **Navigation Menu** shows a link to **Sign Out**:  

<img src="/static/testing/user-stories/home-signedout.png" width="90%" style="margin: 10px;">  
<img src="/static/testing/user-stories/signin.png" width="400px" style="margin: 10px;">  
<img src="/static/testing/user-stories/home-signedin.png" width="90%" style="margin: 10px;">  


* ***As a User, I would like to be able to sign in to the site.***  
The user is able to **Sign In** to the site using the **Sign In** form which can be accessed from **Home Page Alert Links** 
or from the **Sign In** link on the **Navigation Menu**. The **Sign In** form also has a link to the **Register** form. 
Once the **Sign In** form has been populated and the [Form Validation](#form-validation) and checking has been passed, the user is signed in, 
redirected back to the **Home** page, and notified with a message at the top of the screen. 
The **Home Page Alert** is updated to remove the **Sign In** and **Register** links and shows the 
**User Name** of the signed in user. The **Navigation Menu** shows a link to **Sign Out**:  
<img src="/static/testing/user-stories/home-signedout.png" width="90%" style="margin: 10px;">  
<img src="/static/testing/user-stories/signin.png" width="400px" style="margin: 10px;">  
<img src="/static/testing/user-stories/home-signedin.png" width="90%" style="margin: 10px;">  

* ***As a User, I would like to be able to sign out of the site.***  
If the user is **Signed In**, the **Navigation Menu** shows a link to **Sign Out**. If the link is clicked, the user 
is redirected back to the **Home** page and notified with a message at the top of the screen:  
<img src="/static/testing/user-stories/navigation-menu-signedout.png" align="left" width="70%" style="margin: 10px;">
<img src="/static/testing/user-stories/signout-success.png" width="20%" style="margin: 10px;">  

* ***As a User, I am searching for a product which is free from one or more allergens.***  
The user is able to optionally type part or all of a **Product** name into the **Search** input and 
may also optionally select the **Category** and **Allergens** to **Search** based on. Products are 
returned into the product list below. Each product can be viewed in more detail by clicking on 
the **Product Name Link** in the **Product Results Table**.
The **Search** also works if no details are input (all products are returned into the product list). 
Screen prints showing the results of various typical product searches are shown below:  
<img src="/static/testing/user-stories/product-search-1.png" width="90%" style="margin: 10px;">  
<img src="/static/testing/user-stories/product-search-2.png" width="90%" style="margin: 10px;">  
<img src="/static/testing/user-stories/product-search-3.png" width="90%" style="margin: 10px;">  
<img src="/static/testing/user-stories/product-search-4.png" width="90%" style="margin: 10px;">  
<img src="/static/testing/user-stories/product-search-5.png" width="90%" style="margin: 10px;">  
<img src="/static/testing/user-stories/product-search-6.png" width="90%" style="margin: 10px;">  
<img src="/static/testing/user-stories/product-search-7.png" width="90%" style="margin: 10px;">  
<img src="/static/testing/user-stories/product-search-8.png" width="90%" style="margin: 10px;">  

* ***As a User, I have found a product which is free from one or more allergens, and I want to add it to the database.***  
If the user is **Signed In**, they may add a product to the database using the **Add** button on the **Home** page. 
Once the [Form Validation](#form-validation) and checking has been passed, the new **Product** is added to the database and the user is redirected 
to the **Product View** page, and notified with a message at the top of the screen:  
<img src="/static/testing/user-stories/product-add.png" width="400px" align="left" style="margin: 10px;">
<img src="/static/testing/user-stories/product-add-success.png" width="400px" style="margin: 10px;">  

* ***As a User, I have tried a product and would like to rate it.***  
* ***As a User, I have tried a product and would like to review it.***  
If the user is **Signed In**, they may rate and review products on the **Product View** page. 
Once the [Form Validation](#form-validation) and checking has been passed and the review and rating has been 
succesfully added, the user is notified with a message at the top of the screen:  
<img src="/static/testing/user-stories/product-rate-review.png" width="400px" align="left" style="margin: 10px;">
<img src="/static/testing/user-stories/product-rate-review-success.png" width="400px" style="margin: 10px;">  

* ***As a User, I would like to edit an existing product.***
If the user is **Signed In**, they may **Edit** a product by clicking the **Edit Product** button from the **Product View** 
page. The **Product Edit** form is presented, and once the [Form Validation](#form-validation) and checking has been passed and the product has been 
successfully updated, the user is redirected to the **Product View** page for the updated **Product**, 
and is notified with a message at the top of the screen:  
<img src="/static/testing/user-stories/product-edit.png" width="400px" align="left" style="margin: 10px;">
<img src="/static/testing/user-stories/product-edit-success.png" width="400px" style="margin: 10px;">  

* ***As a User, I would like to delete an existing product.***
If the user is **Signed In**, they may **Delete** a product that they have added. If the user is **Signed In** with **Admin** 
privileges, they may **Delete** any product from the database. The **Product Delete** feature is accessed from the **Product Edit** form, 
using the **Delete** button. If the **Delete** button is clicked, the user is asked to confirm that they want to **Delete** the **Product**. 
If the user clicks **Cancel**, they are redirected back to the **Product Edit** form. If the user clicks **Delete**, the product is 
deleted from the database and the user is redirected to the **Home** page and notified with a message at the top of the screen:  
<img src="/static/testing/user-stories/product-delete.png" width="400px" style="margin: 10px;">  
<img src="/static/testing/user-stories/product-delete-confirm.png" width="80%" style="margin: 10px;">  
<img src="/static/testing/user-stories/product-delete-success.png" width="200px" style="margin: 10px;">  

* ***As a User, I would like to add a new product category.***
If the user is **Signed In** and has **Admin** privileges, the **Categories** menu is shown in the **Navigation Menu**. 
The user can pick **Add Category** from the **Categories Menu** and populate the new **Category** name in the form input. 
Once the form has passed [Form Validation](#form-validation) and checking and the new **Category** has been succesfully added, 
the user is redirected to the **Home** page and is notified with a message at the top of the screen:  
<img src="/static/testing/user-stories/category-add.png" width="400px" style="margin: 10px;">  
<img src="/static/testing/user-stories/category-add-success.png" width="200px" style="margin: 10px;">  

* ***As a User, I would like to edit an existing product category.***
If the user is **Signed In** and has **Admin** privileges, the **Categories** menu is shown in the **Navigation Menu**. 
The user can pick **Edit Category** from the **Categories Menu**, pick the **Category** to edit from the **Category Selector**
and populate the new **Category** name in the form input. 
Once the form has passed [Form Validation](#form-validation) and checking and the **Category** has been succesfully edited, 
the user is redirected to the **Home** page and is notified with a message at the top of the screen:  
<img src="/static/testing/user-stories/category-edit.png" width="400px" style="margin: 10px;">  
<img src="/static/testing/user-stories/category-edit-success.png" width="200px" style="margin: 10px;">  

* ***As a User, I would like to delete an existing product category.***
If the user is **Signed In** and has **Admin** privileges, the **Categories** menu is shown in the **Navigation Menu**. 
The user can pick **Delete Category** from the **Categories Menu**, and pick the **Category** name to delete from the 
**Category Selector**. If the **Delete** button is clicked, the user is asked to confirm that they want to **Delete** the **Category**. 
If the user clicks **Cancel**, they are redirected back to the **Category Delete** form. If the user clicks **Delete**, the **Category** is 
deleted from the database, the user is redirected to the **Home** page and is notified with a message at the top of the screen:  
<img src="/static/testing/user-stories/category-delete.png" width="400px" style="margin: 10px;">  
<img src="/static/testing/user-stories/category-delete-confirm.png" width="80%" style="margin: 10px;">
<img src="/static/testing/user-stories/category-delete-success.png" width="200px" style="margin: 10px;">  

* ***As a User, I would like to add a new allergen.***  
If the user is **Signed In** and has **Admin** privileges, the **Allergens** menu is shown in the **Navigation Menu**. 
The user can pick **Add Allergen** from the **Allergens Menu** and populate the new **Allergen** name in the form input. 
Once the form has passed [Form Validation](#form-validation) and checking and the new **Allergen** has been added, the user is redirected to the 
**Home** page and is notified with a message at the top of the screen:  
<img src="/static/testing/user-stories/allergen-add.png" width="400px" style="margin: 10px;">  
<img src="/static/testing/user-stories/allergen-add-success.png" width="200px" style="margin: 10px;">  

* ***As a User, I would like to edit an existing allergen.***
If the user is **Signed In** and has **Admin** privileges, the **Allergens** menu is shown in the **Navigation Menu**. 
The user can pick **Edit Allergen** from the **Allergen Menu**, pick the **Allergen** to edit from the **Allergen Seelctor**  
and populate the new **Allergen** name in the form input. 
Once the form has passed [Form Validation](#form-validation) and checking and the **Allergen** has been succesfully edited, the user is notified with a message 
at the top of the screen:  
<img src="/static/testing/user-stories/allergen-edit.png" width="400px" style="margin: 10px;">  
<img src="/static/testing/user-stories/allergen-edit-success.png" width="200px" style="margin: 10px;">  

* ***As a User, I would like to delete an existing allergen.***
If the user is **Signed In** and has **Admin** privileges, the **Allergens** menu is shown in the **Navigation Menu**. 
The user can pick **Delete Allergen** from the **Allergens Menu**, and pick the **Allergen** name to delete from the 
**Allergen Selector**. If the **Delete** button is clicked, the user is asked to confirm that they want to **Delete** the **Allergen**. 
If the user clicks **Cancel**, they are redirected back to the **Allergen Delete** form. If the user clicks **Delete**, the **Allergen** is 
deleted from the database and the user is notified with a message at the top of the screen:  
<img src="/static/testing/user-stories/allergen-delete.png" width="400px" style="margin: 10px;">  
<img src="/static/testing/user-stories/allergen-delete-confirm.png" width="80%" style="margin: 10px;">
<img src="/static/testing/user-stories/allergen-delete-success.png" width="200px" style="margin: 10px;">  

* ***As a User, I would like to be able to contact the developer.***   
The user may access the **Contact Form** from the **Footer Link**. If the user is **Signed In**, their email address is populated 
automatically. Once the user has populated the **Contact Form** and the form has passed [Form Validation](#form-validation) and checking and has 
been succesfully submitted, a message is displayed at the top of the screen:  
<img src="/static/testing/user-stories/contact-developer.png" width="300px" style="margin: 10px;">  
<img src="/static/testing/user-stories/contact-developer-success.png" width="200px" style="margin: 10px;">  
<img src="/static/testing/user-stories/contact-developer-email.png" width="500px" style="margin: 10px;">  

## Manual Testing ##
The site has been manually tested thoroughly over a 3 week period. See [Bugs Fixed During Testing](#bugs-fixed-during-testing) 
for bugs uncovered and fixed during the manual testing process. Please note that an account with **Admin** privileges has been 
created for testing purposes. This will facilitate testing of features which require **Admin** privileges. 
The username is *testadmin1* and the password is *testadmin1*.


### Features ###
The following **Features** have been explicitly tested:

* **FreeFrom** logo link has been tested and links to home page if selected:  
<img src="/static/testing/logo.png" width="300px" style="margin: 10px;">  

* **Home Page Alert Links** have been tested and function correctly including hover styling, linking to **Sign In** and **Register** pages:  
<img src="/static/testing/home-alert-new.png" width="700px" style="margin: 10px;">  

* **Navigation Menu** has been tested and works as intended. When user is not **Signed In**, **Home** and **Sign in** links are displayed and 
the links function correctly. If user is **Signed In** but does not have **Admin** privileges, **Home** and **Sign Out** links are displayed 
and function correctly. If user is **Signed In** and has **Admin** privileges, **Home**, **Allergens**, **Categories**, and **Sign Out** links 
are displayed and function correctly. **Allergens** and **Categories** drop down menus function correctly. 
**Navigation Menu Hover Styling** has been implemented and is working as intended:  
<img src="/static/testing/navigation-menu-guest.png" width="150px" style="margin: 10px;">
<img src="/static/testing/navigation-menu-user.png" width="150px" style="margin: 10px;">
<img src="/static/testing/navigation-menu-admin.png" width="400px" style="margin: 10px;"> 

* **Search Input**, has been tested and functions correctly, allowing user to optionally input product search criteria to filter search results:  
<img src="/static/testing/search.png" width="500px" style="margin: 10px;">  

* **Category Selector** has been tested and functions correctly, allowing user to optionally select category to filter search results:  
<img src="/static/testing/category.png" width="500px" style="margin: 10px;">  

* **Search Button** functions correctly (including hover styling) and returns matched products in the **Product Results Table**. 
Resizes if user is not signed in and add button is not displayed:  
<img src="/static/testing/search-button.png" width="100px" style="margin: 10px;">  

* **Add Button** functions correctly (including hover styling) and links to the **Product Add** form. Only shown if user is signed in:  
<img src="/static/testing/add-button.png" width="100px" style="margin: 10px;">  

* **Allergen Selector** functions correctly and allows user to optionally select allergens to filter search results:  
<img src="/static/testing/allergen-selector.png" width="80%" style="margin: 10px;">  

* **Product Results Table** functions correctly and displays product search results as expected. 
**Product** name link has been tested and links to **Product View** page:
<img src="/static/testing/results-table.png" width="80%" style="margin: 10px;"> 

* **Sign In** functions correctly (including [Form Validation](#form-validation) and button **Hover Styling**) and enables user to sign in. 
Link to **Register** functions correctly (including hover styling):  
<img src="/static/testing/signin.png" width="500px" style="margin: 10px;"> 

* **Register** form functions correctly (including [Form Validation](#form-validation) and button **Hover Styling**) and allows user to register:  
<img src="/static/testing/register.png" width="500px" style="margin: 10px;"> 

* **Product View** functions correctly and displays product details. If user is not **Signed In**, displays links to **Sign In** and 
**Register** forms. Links function correctly (including hover styling).
If user is signed in, **Review** and **Rating** inputs and buttons are displayed as intended and function 
correctly (including form validation and hover styling).   
**Add** button functions as intended (including [Form Validation](#form-validation) and hover styling), enabling user to review and rate product.  
**Add** button text functions as intended and is changed to **Update** if the user has already reviewed the product.  
**Update** button functions as intended (including form validation and hover styling) and updates review and rating if the product 
has already been reviewed by the user.  
**Edit Product** button is displayed if user is **Signed In** and functions correctly (including hover styling), linking to **Product Edit** page.  
**Add Product** button is displayed if user is **Signed In** and functions correctly (including hover styling), to **Product Add** page.  
User reviews are displayed as intended below in the **User Reviews Table**:  
<img src="/static/testing/product-view-signedout.png" width="500px" style="margin: 10px;">  
<img src="/static/testing/product-view-update-review-new.png" width="500px" style="margin: 10px;">  
  
* **Product Edit** form functions correctly (including [Form Validation](#form-validation) and button **Hover Styling**). 
**Delete** button is shown if the product has been added by the signed in **User**, or if the signed in **User** has **Admin** privileges:  
<img src="/static/testing/product-edit.png" width="500px" style="margin: 10px;">  

* **Product Delete Confirm** form functions correctly (including button **Hover Styling**):  
<img src="/static/testing/product-delete-confirm.png" width="800px" style="margin: 10px;">  

* **Product Add** form functions correctly (including [Form Validation](#form-validation) and button **Hover Styling**):  
<img src="/static/testing/product-add.png" width="500px" style="margin: 10px;">  

* **Allergen Add** form functions correctly (including [Form Validation](#form-validation) and button **Hover Styling**):  
<img src="/static/testing/allergen-add.png" width="500px" style="margin: 10px;">  

* **Allergen Edit** form functions correctly (including [Form Validation](#form-validation) and button **Hover Styling**):  
<img src="/static/testing/allergen-edit.png" width="500px" style="margin: 10px;">  

* **Allergen Delete** form functions correctly (including [Form Validation](#form-validation) and button **Hover Styling**):  
<img src="/static/testing/allergen-delete.png" width="500px" style="margin: 10px;">  

* **Allergen Delete Confirm** form functions correctly (including button **Hover Styling**):  
<img src="/static/testing/allergen-delete-confirm.png" width="800px" style="margin: 10px;">  

* **Category Add** form functions correctly (including [Form Validation](#form-validation) and button **Hover Styling**):  
<img src="/static/testing/category-add.png" width="500px" style="margin: 10px;">  

* **Category Edit** form functions correctly (including [Form Validation](#form-validation) and button **Hover Styling**):  
<img src="/static/testing/category-edit.png" width="500px" style="margin: 10px;">  

* **Category Delete** form functions correctly (including [Form Validation](#form-validation) and button **Hover Styling**):  
<img src="/static/testing/category-delete.png" width="500px" style="margin: 10px;">  

* **Category Delete Confirm** form functions correctly (including button **Hover Styling**):  
<img src="/static/testing/category-delete-confirm.png" width="800px" style="margin: 10px;">  

* **Footer Contact Developer Link** functions correctly (including **Hover Styling**) and links to **Contact Developer** form:  
<img src="/static/testing/contact-link.png" width="150px" style="margin: 10px;">  

* **Footer GitHub Link** functions correctly (including **Hover Styling**) and links to developer page on [GitHub](https://github.com/richardhenyash):  
<img src="/static/testing/github-link.png" width="40px" style="margin: 10px;">  

* **Contact Developer** form functions correctly (including [Form Validation](#form-validation) and button **Hover Styling**), enabling developer to be contacted by email:  
<img src="/static/testing/user-stories/contact-developer.png" width="300px" style="margin: 10px;">  
<img src="/static/testing/user-stories/contact-developer-success.png" width="200px" style="margin: 10px;">  
<img src="/static/testing/user-stories/contact-developer-email.png" width="400px" style="margin: 10px;">

* **Error Page** functions correctly and returns a customised error message and link to the **Home** page if an error is encountered. 
Link hover styling functions correctly:  
<img src="/static/testing/error-page-not-found.png" width="400px" align="left" style="margin: 10px;">
<img src="/static/testing/error-product-not-found.png" width="400px" style="margin: 10px;">  

### Form Validation ###
Validation for all **Forms** implemented using [WTForms](https://wtforms.readthedocs.io/en/2.3.x/) and **Python** has been 
thoroughly manually tested. See [Form Validation Testing Screen Prints](/static/testing/forms), a selection of which are shown below:  
<img src="/static/testing/forms/product-add-form-validation.png" width="600px" style="margin: 10px;">  
<img src="/static/testing/forms/allergen-add-form-validation.png" width="600px" style="margin: 10px;">  
<img src="/static/testing/forms/register-form-validation.png" width="500px" style="margin: 10px;">  
<img src="/static/testing/forms/contact-form-validation.png" width="500px" style="margin: 10px;">  

### Responsive Design ###
* Responsive design has been tested by using [Chrome DevTools](https://developers.google.com/web/tools/chrome-devtools) 
to emulate viewing the website on a number of devices with varying screen dimensions, 
including iPhone 5/SE, iPhone 6/7/8, iPhone 6/7/8 plus, iPhone 11, iPad, iPad Pro, Moto G4, Galaxy S5, Surface Duo, 
Galaxy Fold, Widescreen Laptop and Desktop PC. 
See [Responsive Design Testing](/static/testing/responsive/) screen prints, a selection of which are shown below:  
<img src="/static/testing/responsive/home-phone.png" width="300px" align="left" style="margin: 10px;">
<img src="/static/testing/responsive/product-view-phone.png" width="300px" style="margin: 10px;">  
<img src="/static/testing/responsive/home-ipad.png" width="300px" align="left" style="margin: 10px;">
<img src="/static/testing/responsive/product-view-ipad.png" width="300px" style="margin: 10px;">  
<img src="/static/testing/responsive/home-medium.png" width="300px" align="left" style="margin: 10px;">
<img src="/static/testing/responsive/product-view-medium.png" width="300px" style="margin: 10px;">  
<img src="/static/testing/responsive/home-widescreen.png" width="300px" align="left" style="margin: 10px;">
<img src="/static/testing/responsive/product-view-widescreen.png" width="300px" style="margin: 10px;">  


* Responsive design was then further tested using the 
[Responsive Viewer](https://chrome.google.com/webstore/detail/responsive-viewer/inmopeiepgfljkpkidclfgbgbmfcennb?hl=en)
plug in for chrome. This emulates viewing the website on a large number of devices, 
including iPhone XR, iPhone XS Max, iPhone XS, iPhone X, Galaxy S9 Plus, Galaxy S8 Plus, Galaxy S9, Note 8, Note S8, Pixel 3 and Pixel 3XL.  
See [Responsive Design Testing](/static/testing/responsive) screen prints, a selection of which are also shown below:  
<img src="/static/testing/responsive/responsive-viewer-home-phone1.png" width="300px" align="left" style="margin: 10px;">
<img src="/static/testing/responsive/responsive-viewer-home-phone2.png" width="300px" style="margin: 10px;">  
<img src="/static/testing/responsive/responsive-viewer-product-edit-phone1.png" width="300px" align="left" style="margin: 10px;">
<img src="/static/testing/responsive/responsive-viewer-product-edit-phone2.png" width="300px" style="margin: 10px;">   

The following **Responsive** features were specifically tested:
* The **Navigation Menu** collapses as intended to an icon on small devices less than 768 pixels wide:  
<img src="/static/testing/responsive/navigation-menu-phone-collapsed.png" width="250px" style="margin: 10px;">  

* The **Search Input**, **Category Selector**, **Search Button** and **Add Button** stack as intended on small devices less than 768 pixels wide.  
<img src="/static/testing/responsive/home-stacked.png" width="400px" style="margin: 10px;">  

* The **Product Results Table** and **User Reviews Table** columns collapse on smaller devices as intended:  
<img src="/static/testing/responsive/search-results-collapsed.png" width="300px" align="left" style="margin: 10px;">
<img src="/static/testing/responsive/reviews-collapsed.png" width="250px" style="margin: 10px;">  

### Browser Compatibility Testing ###
The website was tested on the following browsers and operating systems, 
using a combination of manual testing across various devices and the [Browserstack](https://www.browserstack.com/) emulator:
* [Google Chrome](https://www.google.com/intl/en_uk/chrome/) ([Windows 10](https://www.microsoft.com/en-us/windows), [Android 11](https://www.android.com/android-11/) and [Mac OS Big Sur](https://www.apple.com/uk/macos/big-sur/)).
* [Microsoft Edge](https://www.microsoft.com/en-us/edge) ([Windows 10](https://www.microsoft.com/en-us/windows) and [Mac OS Big Sur](https://www.apple.com/uk/macos/big-sur/)).
* [Microsoft Internet Explorer 11](https://support.microsoft.com/en-us/topic/internet-explorer-downloads-d49e1f0d-571c-9a7b-d97e-be248806ca70#ID0EBBD=Windows_10) ([Windows 10](https://www.microsoft.com/en-us/windows)).
* [Safari](https://www.apple.com/uk/safari/) ([Mac OS Big Sur](https://www.apple.com/uk/macos/big-sur/) and [iOS](https://www.apple.com/uk/ios/ios-14/)).
* [Firefox](https://www.mozilla.org/en-GB/firefox/new/) ([Windows 10](https://www.microsoft.com/en-us/windows) and [Mac OS Big Sur](https://www.apple.com/uk/macos/big-sur/)).
* [Opera](https://www.opera.com/) ([Windows 10](https://www.microsoft.com/en-us/windows) and [Mac OS Big Sur](https://www.apple.com/uk/macos/big-sur/)).  

No issues were uncovered during **Browser Compatibility Testing**.

### Bugs Fixed During Testing ###
* **Search Input**, **Category Selector**,  and **Allergen Selector** now populate with previously selected values when search results are displayed.
* **Product Results Table**, **Allergen Selector** and **Category Selector** are now sorted in alphabetic order.
* A missing CSS class was added to the **Edit Product** button.
* A bug was fixed where **Products** rating one star were not correctly displayed in the **Product Results Table**.
* On the **Product View** form, newly added user **Reviews** and **Ratings** are now added or updated in the 
**Reviews Table** after hitting the **Add** or **Update** button.
* The **Product Add** route was updated to redirect to the **Product View** of the successfully added product. 
* The **Category Edit** and **Allergen Edit** routes were updated to populate the **Category** or **Allergen** selector with previously selected values if the **Edit** form fails **Validation** or **Checking**.

### Bugs Remaining ###
* There are no known bugs remaining.