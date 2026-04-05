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
@login_required
def add_task():
    form = TaskForm()

    if form.validate_on_submit():
        try:
            deadline = datetime.combine(
                form.due_date.data,
                form.deadline.data
            )

            new_task = Todo(
                title=form.title.data,
                description=form.description.data,
                due_date=form.due_date.data,
                deadline=deadline,
                user_id=current_user.id
            )

            db.session.add(new_task)
            db.session.commit()

            flash('Task added successfully!', 'success')
            return redirect(url_for('task.dashboard'))

        except Exception as e:
            print("ERROR:", e)
            flash('Error occurred!', 'danger')

    return render_template('add_task.html', form=form)
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
    task = Todo.query.get_or_404(task_id)

    if task.user_id != current_user.id:
        flash('Not authorized!', 'danger')
        return redirect(url_for('task.dashboard'))

    task.status = 'completed' if task.status == 'pending' else 'pending'
    db.session.commit()
    flash('Task updated!', 'success')

#----------------EDIT TASK---------------------------------
@task_bp.route('/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Todo.query.get_or_404(task_id)

    if task.user_id != current_user.id:
        flash('Not authorized!', 'danger')
        return redirect(url_for('task.dashboard'))

    form = TaskForm(obj=task)

    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.due_date = form.due_date.data
        task.deadline = datetime.combine(
            form.due_date.data,
            form.deadline.data
        )

        db.session.commit()
        flash('Task updated!', 'success')
        return redirect(url_for('task.dashboard'))

    return render_template('add_task.html', form=form)