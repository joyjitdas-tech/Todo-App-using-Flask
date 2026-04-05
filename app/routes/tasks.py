from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Todo
from app import db
from datetime import datetime
from app.forms import TaskForm 

task_bp = Blueprint('task', __name__)

# ---------------- Dashboard ----------------
@task_bp.route('/dashboard')
@login_required
def dashboard():
    # Correct query using user_id
    todos = Todo.query.filter_by(user_id=current_user.id).order_by(Todo.deadline).all()
    return render_template('dashboard.html', todos=todos)

# ---------------- Add Task ----------------
  # make sure this exists

@task_bp.route('/add', methods=['GET', 'POST'])
@task_bp.route('/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def add_edit_task(task_id=None):

    if task_id:
        task = Todo.query.get_or_404(task_id)
        if task.user_id != current_user.id:
            return redirect(url_for('task.dashboard'))
        form = TaskForm(obj=task)
    else:
        task = None
        form = TaskForm()

    if form.validate_on_submit():

        if task:  # 🔥 EDIT MODE
            task.title = form.title.data
            task.description = form.description.data
            task.due_date = form.due_date.data
            task.deadline = datetime.combine(form.due_date.data, form.deadline.data)

        else:  # 🔥 ADD MODE
            task = Todo(
                title=form.title.data,
                description=form.description.data,
                due_date=form.due_date.data,
                deadline=datetime.combine(form.due_date.data, form.deadline.data),
                user_id=current_user.id
            )
            db.session.add(task)

        db.session.commit()
        return redirect(url_for('task.dashboard'))

    return render_template('add_task.html', form=form, task=task, edit=(task is not None))
# ---------------- Delete Task ----------------
@task_bp.route('/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Todo.query.get_or_404(task_id)

    if task.user_id != current_user.id:
        flash('Not authorized!', 'danger')
        return redirect(url_for('task.dashboard'))

    db.session.delete(task)
    db.session.commit()
    flash('Task deleted!', 'success')
    return redirect(url_for('task.dashboard'))

# ---------------- Toggle Task Status ----------------
@task_bp.route('/toggle/<int:task_id>', methods=['POST'])
@login_required
def toggle_task(task_id):
    try:
        task = Todo.query.get_or_404(task_id)

        # Check authorization
        if task.user_id != current_user.id:
            return '', 403  # Forbidden

        # Toggle status
        task.status = 'completed' if task.status == 'pending' else 'pending'
        db.session.commit()

        # Return empty 200 OK response for JS
        return '', 200

    except Exception as e:
        # Print for debugging in terminal
        print("TOGGLE ERROR:", e)
        # Return 500 response
        return str(e), 500

#----------------EDIT TASK---------------------------------
# routes/tasks.py
# @task_bp.route('/edit/<int:task_id>', methods=['GET', 'POST'])
# @login_required
# def edit_task(task_id):
#     task = Todo.query.get_or_404(task_id)
#     if task.user_id != current_user.id:
#         flash('Not authorized!', 'danger')
#         return redirect(url_for('task.dashboard'))

#     form = TaskForm(obj=task)

#     if form.validate_on_submit():
#         task.title = form.title.data
#         task.description = form.description.data
#         task.due_date = form.due_date.data
#         task.deadline = datetime.combine(form.due_date.data, form.deadline.data)
#         db.session.commit()
#         flash('Task updated!', 'success')
#         return redirect(url_for('task.dashboard'))

#     return render_template('add_task.html', form=form, edit=True,task=task)