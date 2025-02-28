from django.shortcuts import render, redirect

from shop.models import Animal, Category
# Create your views here.
def animals(request):
    animals = Animal.objects.all()
    categories = Category.objects.all()
    return render(request, 'animals.html', {'animals': animals, 'categories': categories})

def animal_detail(request, animal_id):
    animal = Animal.objects.get(id=animal_id)
    return render(request, 'animal_detail.html', {'animal': animal})


def cow_list(request):
    cows = Animal.objects.all()
    categories = Category.objects.all()
    return render(request, 'cows/cows.html', {'cows': cows, 'categories': categories})


def cow_detail(request, animal_id):
    animal = Animal.objects.get(id=animal_id)
    return render(request, 'cows/cow_detail.html', {'animal': animal})


def new_cow(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        species = request.POST.get('species')
        age = request.POST.get('age')
        weight = request.POST.get('weight')
        status = request.POST.get('status')
        description = request.POST.get('description')
        animal_type = request.POST.get('animal_type')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        medical_certificate = request.FILES.get('medical_certificate')
        quantity = request.POST.get('quantity')
        gender = request.POST.get('gender')

        category = Category.objects.get(id=category_id)
        
        animal = Animal.objects.create(
            name=name, 
            category=category, 
            age=age, 
            weight=weight, 
            status=status, 
            description=description, 
            animal_type=animal_type, 
            price=price, 
            image=image, 
            medical_certificate=medical_certificate, 
            quantity=quantity, 
            gender=gender, 
            species=species, 
        )
        animal.save()
        return redirect('cows')
            
    return render(request, 'cows/new_cow.html')


def edit_cow(request):
    if request.method == 'POST':
        animal_id = request.POST.get('animal_id')
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        species = request.POST.get('species')
        age = request.POST.get('age')
        weight = request.POST.get('weight')
        status = request.POST.get('status')
        description = request.POST.get('description')
        animal_type = request.POST.get('animal_type')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        medical_certificate = request.FILES.get('medical_certificate')
        quantity = request.POST.get('quantity')
        gender = request.POST.get('gender')

        category = Category.objects.get(id=category_id)
        animal = Animal.objects.get(id=animal_id)
        animal.name = name
        animal.category = category
        animal.species = species
        animal.age = age
        animal.weight = weight
        animal.status = status
        animal.description = description
        animal.animal_type = animal_type
        animal.price = price
        animal.image = image
        animal.medical_certificate = medical_certificate
        animal.quantity = quantity
        animal.gender = gender
        animal.save()
        return redirect('cows')
    return render(request, 'cows/edit_cow.html')
