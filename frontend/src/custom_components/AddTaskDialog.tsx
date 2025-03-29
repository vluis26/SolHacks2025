import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter, DialogDescription } from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { useState, useEffect } from "react"
import { RadioGroupItem, RadioGroup } from "@/components/ui/radio-group"
import { Label } from "@/components/ui/label"
import { format } from "date-fns"
import { CalendarIcon } from "lucide-react"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Calendar } from "@/components/ui/calendar"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover"

type AddTaskDialogProps = {
    isOpen: boolean
    onClose: () => void
    courseId: number
    onAddTask: (courseId: number, task: any) => void
}

const AddTaskDialog: React.FC<AddTaskDialogProps> = ({ isOpen, onClose, courseId, onAddTask}) => {
    const [name, setName] = useState("")
    const [type, setType] = useState("assignment")
    const [date, setDate] = useState<Date | undefined>(undefined)
    const [open, setOpen] = useState(false)

    useEffect(() => {
        if (!isOpen) {
            setName("")
            setType("assignment")
            setDate(undefined)
            setOpen(false)
        }
    }, [isOpen])

    const handleSubmit = () => {
        const newTask = {
            id: Date.now(),
            title: name,
            type: type,
            dueDate: format(date!, "MMM d, yyyy"),
            note: ""
        }
        console.log(newTask)

        onAddTask(courseId, newTask)

        setName("")
        setType("assignment")
        setDate(undefined)
        
        onClose()
    }

    const DatePicker = () => {
        return (
            <Popover open={open} onOpenChange={setOpen}>
                <PopoverTrigger asChild>
                    <Button
                        type="button"
                        variant="outline"
                        className={cn(
                            "w-full justify-start text-left font-normal",
                            !date && "text-muted-foreground"
                        )}
                    >
                        <CalendarIcon className="mr-2 h-4 w-4" />
                        {date ? format(date, "PPP") : <span>Pick a date</span>}
                    </Button>
                </PopoverTrigger>
                <PopoverContent className="w-auto p-0" align="start">
                    <Calendar
                        mode="single"
                        selected={date}
                        onSelect={(day) => {
                            setDate(day)
                            setOpen(false)
                        }}
                        initialFocus
                    />
                </PopoverContent>
            </Popover>
        )
    }

    return (
        <Dialog open={isOpen} onOpenChange={onClose}>
            <DialogContent className="sm:max-w-[425px]">
                <DialogHeader>
                    <DialogTitle>Add New Task</DialogTitle>
                    <DialogDescription>Create a new task for your course. It will automatically be added to your calendar.</DialogDescription>
                </DialogHeader>
                
                <Label htmlFor="titleInput">Task Name</Label>
                <Input 
                    id="titleInput"
                    placeholder="Enter task name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                />
                <RadioGroup value={type} onValueChange={setType}>
                    <div className="flex items-center space-x-2">
                        <RadioGroupItem value="assignment" id="r1" />
                        <Label htmlFor="r1">Assignment</Label>
                    </div>
                    <div className="flex items-center space-x-2">
                        <RadioGroupItem value="exam" id="r2" />
                        <Label htmlFor="r2">Exam</Label>
                    </div>
                    <div className="flex items-center space-x-2">
                        <RadioGroupItem value="quiz" id="r3" />
                        <Label htmlFor="r3">Quiz</Label>
                    </div>
                </RadioGroup>

                <div className="grid gap-2">
                    <Label>Due Date</Label>
                    <DatePicker />
                </div>

                <DialogFooter>
                    <Button variant="outline" onClick={onClose}>
                        Cancel
                    </Button>
                    <Button onClick={handleSubmit} disabled={!name.trim() || !date}>
                        Add Task
                    </Button>
                </DialogFooter>

            </DialogContent>
        </Dialog>
    )
}

export default AddTaskDialog