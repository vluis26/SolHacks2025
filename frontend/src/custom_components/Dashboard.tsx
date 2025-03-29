import {
    ChevronDown,
    Filter,
    Plus,
    Search,
  } from "lucide-react"
  
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import CourseRow from "./CourseRow"
import courses from "@/courses"

type DashboardProps = {
}

const Dashboard: React.FC<DashboardProps> = () => {
    return (
        <div className="flex flex-col min-h-screen">
        <header className="flex h-14 lg:h-[60px] items-center gap-4 border-b bg-muted/40 px-6">
          <div className="flex items-center gap-2">
            {/* <Image src="/logo.png" alt="SyllaByte Logo" width={32} height={32} /> */}
            <span className="text-xl font-bold">SyllaByte</span>
          </div>
  
          <div className="w-full flex-1 ml-8">
            <div className="relative">
              <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input
                type="search"
                placeholder="Search courses and tasks..."
                className="w-full bg-background shadow-none appearance-none pl-8 md:w-2/3 lg:w-1/3"
              />
            </div>
          </div>
  
          <Button variant="outline" className="ml-auto mr-2 rounded-full px-6">
            Install our extension
          </Button>
  
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="icon" className="rounded-full">
                <Avatar className="h-8 w-8">
                  <AvatarFallback>S</AvatarFallback>
                </Avatar>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem>Profile</DropdownMenuItem>
              <DropdownMenuItem>Settings</DropdownMenuItem>
              <DropdownMenuItem>Logout</DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </header>
  
        <main className="flex-1 overflow-auto p-6">
          <div className="flex items-center justify-between mb-6">
            <h1 className="text-2xl font-bold">Your Courses</h1>
            <div className="flex items-center gap-2">
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="outline" className="gap-1">
                    My SyllaByte
                    <ChevronDown className="h-4 w-4" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent>
                  <DropdownMenuItem>All Courses</DropdownMenuItem>
                  <DropdownMenuItem>Active Courses</DropdownMenuItem>
                  <DropdownMenuItem>Archived Courses</DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
  
              <div className="relative">
                <Input type="search" placeholder="Find courses..." className="w-[250px]" />
                <Search className="absolute right-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
              </div>
  
              <Button variant="outline" className="gap-1">
                <Filter className="h-4 w-4" />
                Filter
              </Button>
  
              <Button>
                <Plus className="mr-2 h-4 w-4" />
                New Course
              </Button>
            </div>
          </div>
  
          <div className="mt-8">
            {courses.map((course) => (
              <CourseRow key={course.id} course={course} />
            ))}
          </div>
  
        </main>
      </div>
    )
}

export default Dashboard