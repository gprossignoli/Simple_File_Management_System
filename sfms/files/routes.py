from flask import Blueprint, render_template
from flask_user import current_user, login_required

from sfms.files.service import FileService, FileAlreadyExistsException
from sfms.files.forms import FileForm


files = Blueprint(name='files', import_name=__name__)


@files.route('/files', methods=['GET', 'POST'])
@login_required
def files_view():
    form = FileForm()
    if form.validate_on_submit():
        file = form.file.data
        try:
            FileService.create_file(file, user_id=current_user.id)
        except FileAlreadyExistsException as e:
            return f'File: {e.filename} already exists!', 400
    files_data = FileService.get_user_files(current_user.id)
    return render_template(template_name_or_list='files.html', files=files_data, form=form)
