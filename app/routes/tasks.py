from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Todo
from app import db
from datetime import datetime

task_bp = Blueprint('task', __name__)

# ---------------- Dashboard ----------------
@task_bp.route('/dashboard')
@login_required
def dashboard():
    # Correct query using user_id
    todos = Todo.query.filter_by(user_id=current_user.id).order_by(Todo.deadline).all()
    return render_template('dashboard.html', todos=todos)

# ---------------- Add Task ----------------
@task_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_task():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        due_date = request.form.get('due_date')  # "YYYY-MM-DD"
        deadline_time = request.form.get('deadline_time')  # "HH:MM"

        if not title or not due_date or not deadline_time:
            flash('Please fill all required fields!', 'danger')
            return redirect(url_for('task.add_task'))

        # Combine date + time for deadline
        deadline_str = f"{due_date} {deadline_time}"
        deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")

        new_task = Todo(
            title=title,
            description=description,
            due_date=datetime.strptime(due_date, "%Y-%m-%d").date(),
            deadline=deadline,
            user_id=current_user.id   # Assign correct user_id
        )

        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully!', 'success')
        return redirect(url_for('task.dashboard'))

    return render_template('add_task.html')

# ---------------- Delete Task ----------------
@task_bp.route('/delete/<int:task_id>')
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
@task_bp.route('/toggle/<int:task_id>')
@login_required
def toggle_task(task_id):
    task = Todo.query.get_or_404(task_id)

    if task.user_id != current_user.id:
        flash('Not authorized!', 'danger')
        return redirect(url_for('task.dashboard'))

    task.status = 'completed' if task.status == 'pending' else 'pending'
    db.session.commit()
    return redirect(url_for('task.dashboard'))