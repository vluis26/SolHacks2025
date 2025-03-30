import { useState } from "react"
import { Task } from "@/types"
import { Card } from "@/components/ui/card"
import { CardContent } from "@/components/ui/card"

import { CardFooter } from "@/components/ui/card"
import { MoreVertical } from "lucide-react"
import { Trash2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { Copy } from "lucide-react"

type TaskCardProps = {
    task: Task,
    onDelete: () => void
}

const TaskCard: React.FC<TaskCardProps> = ({ task, onDelete }) => {
    const [note, setNote] = useState(task.note || "")
    const [isEditing, setIsEditing] = useState(false)

    const getCardColor = (type: string) => {
        switch (type) {
          case "Exam":
            return "border-l-4 border-l-red-500"
          case "Assignment":
            return "border-l-4 border-l-blue-500"
          case "Quiz":
            return "border-l-4 border-l-purple-500"
          default:
            return "border-l-4 border-l-gray-500"
        }
      }
    
  
    return (
        <Card className={`< ${getCardColor(task.type!)}`}>
            <CardContent className="p-4">
                <div className="flex items-start justify-between">
                    <Checkbox id={`task-${task.task_id}`} className="mt-1" />
                    <div className="flex-1 ml-2">
                        <h3 className="font-medium text-lg">{task.name}</h3>
                        {isEditing ? (
                            <div className="mt-2">
                                <textarea
                                    className="w-full text-sm p-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                                    value={note}
                                    onChange={(e) => setNote(e.target.value)}
                                    placeholder="Add your notes here..."
                                    rows={2}
                                    autoFocus
                                    onBlur={() => setIsEditing(false)}
                                />
                            </div>
                        ) : (
                            <div
                                className="text-sm mt-2 p-2 bg-muted/30 rounded-md min-h-[40px] cursor-text"
                                onClick={() => setIsEditing(true)}
                            >
                                {note ? note : <span className="text-muted-foreground italic">Click to add notes...</span>}
                            </div>
                        )}
                        <div className="text-sm text-blue-500 mt-4">Due: {task.due_date}</div>
                    </div>

                    <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                            <Button variant="ghost" size="icon" className="h-8 w-8">
                                <MoreVertical className="h-4 w-4" />
                            </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                            <DropdownMenuItem className="text-destructive" onClick={onDelete}>
                                <Trash2 className="h-4 w-4 mr-2" />
                                Delete
                            </DropdownMenuItem>
                        </DropdownMenuContent>
                    </DropdownMenu>
                </div>

            </CardContent>
            <CardFooter className="flex justify-between p-4 pt-0">
                <div className="flex gap-2 w-full">
                    <Button variant="outline" size="sm" className="h-8 flex-1">
                        <Copy className="h-4 w-4 mr-1" />
                        Copy link
                    </Button>
                    <Button variant="outline" size="sm" className="h-8 flex-1 whitespace-nowrap">
                        Calendar
                    </Button>
                </div>
            </CardFooter>

        </Card>
    )
}

export default TaskCard;