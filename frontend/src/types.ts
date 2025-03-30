export interface Task {
    task_id: string | number
    name: string
    is_completed: boolean
    due_date: string
    note: string
    type: string
    calendar_link: string
}

export interface Course {
    id: number
    title: string
    code: string
    tasks: Task[]
  }
