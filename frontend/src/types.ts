export interface Task {
    id: string | number
    title?: string
    completed?: boolean
    type?: string
    dueDate?: string
    note: string
}

export interface Course {
    id: number
    title: string
    code: string
    tasks: Task[]
  }
  