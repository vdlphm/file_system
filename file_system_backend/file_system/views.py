import json
import django
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound, HttpResponseServerError, JsonResponse
from django.shortcuts import render
from django.db import IntegrityError

#import file_system_backend.file_system.models as md
import file_system.models as md

from django.utils import timezone

# Create your views here.

# find the next to last /
def find(s):
    last_index = -1
    for i, ltr in enumerate(s):
        if ltr == '/' and i != len(s) - 1:
            last_index = i
    return last_index

# check for path validation
def pathValid(path):
    try: 
        path.index('/')
    except ValueError:
        return 'Path is not the the right format. Not having \'/\' in the path.'
    if path[len(path) - 1] != '/':
        return 'Path is not the the right format. Not having \'/\' in the end.'
    return None

# create folder/file
def create(request):
    if request.method == 'POST':
        # retrieve data from request
        jsonData = json.loads(request.body)
        try:
            f_path = jsonData['path']
            f_data = jsonData['data']
        except Exception as ex:
            return HttpResponseBadRequest('Request body is not in the correct format')
        
        # check path validity
        check = pathValid(f_path)
        if check:
             return HttpResponseBadRequest(check)
        
        # find file/folder name from path
        sep_id = find(f_path)
        f_name = f_path[:len(f_path) - 1]
        if sep_id != -1:
            f_name = f_path[sep_id + 1:len(f_path) - 1]
        else:
            if not (f_data is None):
                return HttpResponseBadRequest('File must reside in a folder!')
        
        # retrieve parent folder
        f_dir_path = f_path[:f_path.index((f_name))]
        if sep_id != -1:
            try:
                f_dir = md.Folder.objects.get(path=f_dir_path)
            except md.Folder.DoesNotExist:
                return HttpResponseNotFound('Folder at path <{}> does not exist.'.format(f_dir_path))
        else:
            f_dir = None

        # create file/folder
        try:
            if f_data is None:
                md.Folder(path=f_path, name=f_name, directory=f_dir, create_at=timezone.now()).save()
            else:
                md.File(path=f_path, name=f_name, directory=f_dir, create_at=timezone.now(), data=f_data).save()
        except IntegrityError:
            return HttpResponseForbidden('Folder <{}> already has a file/folder <{}>'.format(f_dir_path, f_name))
        except Exception as ex:
            return HttpResponseServerError('Cannot create file/folder because {}'.format(ex))

        return JsonResponse(status=200, data={'message': 'create successfully'})
    else:
        return HttpResponseBadRequest('Use POST request for create')

# view file content
def catFile(request):
    if request.method == 'GET':
        # retrieve data from request
        jsonData = json.loads(request.body)
        try:
            f_path = jsonData['path']
        except Exception as ex:
            return HttpResponseBadRequest('Request body is not in the right format')
        
        # check path validity
        check = pathValid(f_path)
        if check:
            return HttpResponseBadRequest(check)

        # retrieve file data
        try:
            f_object = md.File.objects.get(path=f_path)
            f_data = f_object.data
        except md.File.DoesNotExist:
            return HttpResponseNotFound('File <{}> does not exist'.format(f_path))
        
        return JsonResponse(status=200, data={'message': 'obtain successfully', 'data': f_data})
    else:
        return HttpResponseBadRequest('Use GET request instead')

# view folder content
def listFolder(request):
    if request.method == 'GET':
        # retrieve data from request
        jsonData = json.loads(request.body)
        try:
            f_path = jsonData['path']
        except Exception as ex:
            return HttpResponseBadRequest('Request body is not in the right format')
        
        # check path validity
        check = pathValid(f_path)
        if check:
            return HttpResponseBadRequest(check)

        # retrieve folder items
        try:
            f_object = md.Folder.objects.get(path=f_path)
            folder_list = md.Folder.objects.filter(directory=f_object).values('name')
            file_list = md.File.objects.filter(directory=f_object).values('name')
            items= []
            
            for folder in folder_list:
                items.append(folder)
            for file in file_list:
                items.append(file)
        except md.Folder.DoesNotExist:
            return HttpResponseNotFound('<{}> does not exist'.format(f_path))
        return JsonResponse(status=200, data={'message': 'obtain successfully', 'data': items})
    else:
        return HttpResponseBadRequest('Use GET request instead')

# helper function for move folder ****
def folderUpdate(folder_obj, new_dir_path):
    all_file = md.File.objects.filter(directory=folder_obj)
    all_folder = md.Folder.objects.filter(directory=folder_obj)
    new_path = new_dir_path + folder_obj.name + '/'
    folder_obj.path = new_path
    folder_obj.save()

    for list in all_file:
        list.path = new_path + list.name + '/'
        list.save()
    for folder in all_folder:
        folderUpdate(folder, new_path)

# move folder/file ****
def moveTo(request):
    if request.method == 'PUT':
        # retireve data from request
        jsonData = json.loads(request.body)
        try:
            f_path = jsonData['path']
            new_dir = jsonData['directory']
        except Exception as ex:
            return HttpResponseBadRequest('Request body is not in the right format')

        # check path validity
        check = pathValid(f_path)
        if check:
            return HttpResponseBadRequest(check)
        check = pathValid(new_dir)
        if check:
            return HttpResponseBadRequest(check)
        
        # check if destination is a child of folder
        try:
            new_dir.index(f_path)
            return HttpResponseForbidden('Cannot move <{}> to <{}> because it\'s parent folder'.format(f_path, new_dir))
        except ValueError:
            pass

        # retrieve new directory
        try:
            new_folder = md.Folder.objects.get(path=new_dir)
        except md.Folder.DoesNotExist:
            return HttpResponseNotFound('<{}> does not exist'.format(new_dir))

        # retrieve file/folder
        done = False
        try:
            f_obj = md.File.objects.get(path=f_path)
            done = True
        except md.File.DoesNotExist:
            pass
        if not done:
            try:
                f_obj = md.Folder.objects.get(path=f_path)
            except md.Folder.DoesNotExist:
                return HttpResponseNotFound('<{}> does not exist'.format(f_path))

        # move file to new folder
        new_path = new_dir + f_obj.name + '/'
        if type(f_obj) is md.File:
            print('move file')
            try:
                f_obj.path = new_path
                f_obj.directory= new_folder
                f_obj.save()
                return JsonResponse(status=200, data={'message': 'move successfully'})
            except IntegrityError:
                return HttpResponseForbidden('Folder <{}> already has file name <{}>'.format(new_folder, f_obj.name))
            except Exception as ex:
                return HttpResponseServerError('Cannot move {}'.format(ex))

        # move folder to new folder
        else:
            try:
                all_folder = md.Folder.objects.filter(directory=f_obj)
                all_file = md.File.object.filter(directory=f_obj)
                f_obj.path = new_path
                f_obj.directory= new_folder
                f_obj.save()

                # update path for every files in folder
                for file in all_file:
                    file.path = new_path + file.name + '/'
                    file.save()
                # recursively paths of every folder in folder
                for folder in all_folder:
                    folderUpdate(folder, new_path)
                return JsonResponse(status=200, data={'message': 'move successfully'})
            except IntegrityError:
                return HttpResponseForbidden('Folder <{}> already has folder name <{}>'.format(new_folder, f_obj.name))
            except Exception as ex:
                return HttpResponseServerError('Cannot move {}'.format(ex))
            
    else:
        return HttpResponseBadRequest('Use PUT request instead')

# delete folder/file
def delete(request):
    # retrieve data from request
    if request.method == 'PUT':
        jsonData = json.loads(request.body)
        try:
            f_path = jsonData['path']
        except Exception as ex:
            return HttpResponseBadRequest('Request is not in the right format')

        # check path validity
        check = pathValid(f_path)
        if check:
            return HttpResponseBadRequest(check)
        
        # retrieve folder/file and delete
        done = False
        try:
            f_obj = md.Folder.objects.get(path=f_path)
            done = True
        except md.Folder.DoesNotExist:
            pass
        if not done:
            try:
                f_obj = md.File.objects.get(path=f_path)
            except md.File.DoesNotExist:
                return HttpResponseNotFound('Folder/file <{}> does not exist'.format(f_path))

        f_obj.delete()
        return JsonResponse(status=200, data={'message': 'delete successfully'})
    else:
        return HttpResponseBadRequest('Use PUT request instead')

# update folder/file ****
def update(request):
    if request.method == 'PUT':
        # retrieve data from request
        jsonData = json.loads(request.body)
        try:
            f_path = jsonData['path']
            new_name = jsonData['name']
            new_data = jsonData['data']
        except Exception as ex:
            return HttpResponseBadRequest('Request body is not in the right format')

        # check path validity
        check = pathValid(f_path)
        if check:
             return HttpResponseBadRequest(check)

        # update file if path points to file
        try:
            f_obj = md.File.objects.get(path=f_path)
            old_name = f_obj.name
            id = f_path.index(old_name)
            new_path = f_path[:id] + new_name + '/'
            f_obj.name = new_name
            f_obj.path = new_path
            if new_data:
                f_obj.data = new_data
            f_obj.save()
            return JsonResponse(status=200, data={'message': 'update successfully'})
        except md.File.DoesNotExist:
            pass
        except IntegrityError:
            return HttpResponseForbidden('Folder <{}> already has file name <{}>'.format(new_folder, f_obj.name))
        except Exception as ex:
            return HttpResponseServerError('Cannot update folder because {}'.format(ex))

        # update folder otherwise
        try:
            f_obj = md.Folder.objects.get(path=f_path)
            folder_list = md.Folder.objects.filter(directory=f_obj)
            file_list = md.File.objects.filter(directory=f_obj)
            old_name = f_obj.name
            id = f_path.index(old_name)
            new_path = f_path[:id] + new_name + '/'
            f_obj.name = new_name
            f_obj.path = new_path
            f_obj.save()
            # rename files
            for file in file_list:
                file.path = new_path + file.name + '/'
                file.save()
            # rename folder and its children path
            for folder in folder_list:
                folderUpdate(folder, new_path)
            return JsonResponse(status=200, data={'message': 'update successfully'})
        except md.Folder.DoesNotExist:
            return HttpResponseNotFound('Folder/file <{}> does not exist'.format(f_path))
        except Exception as ex:
            return HttpResponseServerError('Cannot update file because {}'.format(ex))
    else:
        return HttpResponseBadRequest('Use PUT request instead')