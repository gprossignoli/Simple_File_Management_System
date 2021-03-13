from os import stat
from hashlib import sha256

from flask import Blueprint, render_template
from flask_user import current_user, login_required
from werkzeug.utils import secure_filename

from sfms.files.models import File
from sfms.files.service import FileService
from sfms.files.forms import FileForm


files = Blueprint(name='files', import_name=__name__)


@files.route('/files', methods=['GET', 'POST'])
@login_required
def files_view():
    files_data = FileService.get_user_files(current_user.id)
    form = FileForm()
    if form.validate_on_submit():
        file = form.file.data
        FileService.create_file(file)

    return render_template(template_name_or_list='files.html', files=files_data, form=form)
