import { useState, useEffect } from "react";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import PropTypes from "prop-types";
import api from "../../../api";
import { Card, CardContent, CardHeader, CardTitle } from "../../ui/card";
import { Button } from "../../ui/button";
import { Input } from "../../ui/input";
import { Textarea } from "../../ui/textarea";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "../../ui/dialog";
import { PlusCircle, AlertCircle } from "lucide-react";
import { Alert, AlertDescription } from "../../ui/alert";
import AnnouncementItem from "./AnnouncementItem";

const Announcements = ({ sportId }) => {
  const [announcements, setAnnouncements] = useState([]);
  const [newAnnouncement, setNewAnnouncement] = useState({
    title: "",
    content: "",
    description: "",
    sport: sportId,
  });
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);
  const [deleteId, setDeleteId] = useState(null);
  const userData = JSON.parse(localStorage.getItem("userData"));

  const user_type = userData.profile.user_type;

  useEffect(() => {
    fetchAnnouncements();
  }, [sportId]);

  const fetchAnnouncements = async () => {
    try {
      const response = await api.get(`/sport/${sportId}/posts/`);
      const data = response.data.data;
      setAnnouncements(data);
    } catch (error) {
      console.error("Error fetching announcements:", error);
      toast.error("Error fetching announcements");
    }
  };

  const handleCreate = async () => {
    try {
      // Print the form data in the console
      console.log("Form Data:", newAnnouncement);

      const response = await api.post(`/sport/create-post/`, newAnnouncement);
      if (response.data.status === "success") {
        setNewAnnouncement({
          title: "",
          content: "",
          description: "",
          sport: sportId,
        });
        fetchAnnouncements();
        setIsDialogOpen(false);
        toast.success("Announcement created successfully");
      }
    } catch (error) {
      console.error("Error creating announcement:", error);
      toast.error("Error creating announcement");
    }
  };

  const handleDelete = async () => {
    try {
      const response = await api.delete(`/sport/${deleteId}/delete-post/`);
      if (response.status === 204) {
        setIsDeleteDialogOpen(false);
        setDeleteId(null);
        fetchAnnouncements();
        toast.success("Announcement deleted successfully");
      }
    } catch (error) {
      console.error("Error deleting announcement:", error);
      toast.error("Error deleting announcement");
    }
  };

  const confirmDelete = (id) => {
    setDeleteId(id);
    setIsDeleteDialogOpen(true);
  };

  return (
    <Card className="w-full max-w-4xl mx-auto">
      {console.log(user_type)}
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle className="text-2xl font-bold">Announcements</CardTitle>
        {(user_type === "admin" || user_type === "staff") && (
          <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
            <DialogTrigger asChild>
              <Button>
                <PlusCircle className="mr-2 h-4 w-4" /> Create Announcement
              </Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Create New Announcement</DialogTitle>
              </DialogHeader>
              <div className="space-y-4 py-4">
                <Input
                  type="text"
                  value={newAnnouncement.title}
                  onChange={(e) =>
                    setNewAnnouncement({
                      ...newAnnouncement,
                      title: e.target.value,
                    })
                  }
                  placeholder="Title"
                />
                <Input
                  type="text"
                  value={newAnnouncement.description}
                  onChange={(e) =>
                    setNewAnnouncement({
                      ...newAnnouncement,
                      description: e.target.value,
                    })
                  }
                  placeholder="Description"
                />
                <Textarea
                  value={newAnnouncement.content}
                  onChange={(e) =>
                    setNewAnnouncement({
                      ...newAnnouncement,
                      content: e.target.value,
                    })
                  }
                  placeholder="Content"
                />
                <Button
                  onClick={handleCreate}
                  className="w-full"
                  disabled={
                    !newAnnouncement.title ||
                    !newAnnouncement.description ||
                    !newAnnouncement.content
                  }
                >
                  Create Announcement
                </Button>
              </div>
            </DialogContent>
          </Dialog>
        )}
      </CardHeader>
      <CardContent>
        {announcements.length > 0 ? (
          <div className="space-y-4">
            {announcements.map((announcement) => (
              <AnnouncementItem
                key={announcement.id}
                announcement={announcement}
                onDelete={() => confirmDelete(announcement.id)}
              />
            ))}
          </div>
        ) : (
          <Alert>
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>There are no announcements yet.</AlertDescription>
          </Alert>
        )}
      </CardContent>

      <Dialog open={isDeleteDialogOpen} onOpenChange={setIsDeleteDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Confirm Deletion</DialogTitle>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <p>Are you sure you want to delete this announcement?</p>
            <div className="flex justify-end space-x-2">
              <Button onClick={() => setIsDeleteDialogOpen(false)}>
                Cancel
              </Button>
              <Button onClick={handleDelete} className="bg-red-500 text-white">
                Delete
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>

      <ToastContainer />
    </Card>
  );
};

Announcements.propTypes = {
  sportId: PropTypes.number.isRequired,
};

export default Announcements;