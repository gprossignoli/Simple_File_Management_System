from flask import Blueprint, render_template, request
from flask_user import current_user, login_required
from werkzeug.utils import redirect

from sfms.files.service import FileService, FileAlreadyExistsError, FileNotExistsError, FileInsertionError
from sfms.files.forms import FileForm


files = Blueprint(name='files', import_name=__name__, url_prefix='/files')


@files.route('', methods=['GET', 'POST'])
@login_required
def files_view():
    form = FileForm()
    if form.validate_on_submit():
        file = form.file.data
        try:
            FileService.create_file(file, user_id=current_user.id)
        except FileAlreadyExistsError as e:
            return f'File: {e.filename} already exists!', 400
        except FileInsertionError as e:
            return f'File: {e.filename} insertion failed!', 500
    page = request.args.get('page', 1)
    try:
        if page == "":
            page = 1
        page = int(page)
        if page < 1:
            page = 1

    except TypeError:
        return f'Page parameter not valid, must be integer', 400

    files_data, prev_page, next_page = FileService.get_user_files(user_id=current_user.id, current_page=page)



    return render_template(template_name_or_list='files.html', files=files_data, form=form,
                           next_page=next_page, prev_page=prev_page)


@files.route('/delete/<string:filename>', methods=['POST', 'DELETE'])
@login_required
def delete_file(filename):
    try:
        file = FileService.get_file_by_title(filename)
    except FileNotExistsError as e:
        return f'File: {e.filename} does not exists!', 404
    FileService.delete_file(file)
    return redirect('/files')


@files.route('/download/<string:filename>', methods=['POST'])
@login_required
def download_file(filename):
    try:
        file = FileService.get_file_from_disk(filename)
    except FileNotExistsError as e:
        return f'File: {e.filename} does not exists!', 404
    return file
