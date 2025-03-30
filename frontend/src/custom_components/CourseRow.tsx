import { Course } from "@/types"
import TaskCard from "./TaskCard"
import AddTaskDialog from "./AddTaskDialog"

import { useState } from "react"
import {
  Plus
} from "lucide-react"

import { Button } from "@/components/ui/button"
import {
    Carousel,
    CarouselContent,
    CarouselItem,
    CarouselNext,
    CarouselPrevious,
  } from "@/components/ui/carousel"


type CourseRowProps = {
    course: Course
}

const CourseRow: React.FC<CourseRowProps> = ({ course }) => {
        const [tasks, setTasks] = useState(course.tasks)
        const [addTaskOpen, setAddTaskOpen] = useState(false)

      
        const handleDeleteTask = (taskId: number) => {
          const newTasks = tasks.filter((task) => task.task_id !== taskId)
          setTasks(newTasks)
        }
      
        const handleAddTask = (courseId: number, newTask: any) => {
            const updatedTasks = [...tasks, newTask]

            updatedTasks.sort((a, b) => {
              const dateA = new Date(a.dueDate)
              const dateB = new Date(b.dueDate)
              return dateA.getTime() - dateB.getTime()
            })
          
            setTasks(updatedTasks)        
        }
      
        return (
          <div className="mb-8">
            <div className="flex items-center justify-between mb-4">
                <div>
                    <h2 className="text-xl font-semibold">{course.title}</h2>
                    <p className="text-sm text-muted-foreground">{course.code}</p>
                </div>
                <Button variant="outline" size="sm" onClick={() => setAddTaskOpen(true)}>
                    <Plus className="h-4 w-4 mr-1" />
                    Add Task
                </Button>

              <AddTaskDialog
                isOpen={addTaskOpen}
                onClose={() => setAddTaskOpen(false)}
                courseId={course.id}
                onAddTask={handleAddTask}
              />
            </div>
      
            <div className="max-w-6xl">
                <Carousel className="w-full ml-10 mr-10">
                    <CarouselContent className="">
                        {tasks.map((task: any) => (
                            <CarouselItem key={task.id} className="pl-4 md:basis-1/2 lg:basis-1/3">
                                <TaskCard key={task.id} task={task} onDelete={() => handleDeleteTask(task.id)} />
                            </CarouselItem>
                        ))}
                    </CarouselContent>
                    <CarouselPrevious />
                    <CarouselNext />
                </Carousel>
            </div>
          </div>
        )
    
}

export default CourseRow
