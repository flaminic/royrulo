from  MySQLdb import connect, cursors
import uuid
import os

class Database:
    def __init__(self):
        self.database_host = os.getenv("DATABASE_HOST") or "localhost"
        self.database_user = os.getenv("DATABASE_USER") or "root"
        self.database_password = os.getenv("DATABASE_PASSWORD") or ""
        self.database_name = os.getenv("DATABASE_NAME") or "royrulo"
        self.con = None

    def _connect(self):
        self.con = connect(host=self.database_host, user=self.database_user, passwd=self.database_password,
                           db=self.database_name, cursorclass=cursors.DictCursor)
        return self.con.cursor()

    def _disconnect(self):
        self.con.close()

    def get_person_details(self, person_id):
        cur = self._connect()
        cur.execute("SELECT id, guestName, email, howMany, diet FROM rsvp WHERE id = %s", (person_id,))
        person_details = cur.fetchone()
        self._disconnect()
        return person_details

    def get_all_people(self):
        cur = self._connect()
        cur.execute("SELECT id, guestName, email, howMany, diet FROM rsvp")
        people = cur.fetchall()
        self._disconnect()
        return people

    def insert_person(self, **person_details):
        try:
            person_id = uuid.uuid4()
            cur = self._connect()
            cur.execute(
                "INSERT INTO rsvp (id, guestName, email, howMany, diet) VALUES (%s,%s,%s,%s,%s)",
                (str(person_id),
                 person_details['guest_name'],
                 person_details['email'],
                 person_details['how_many'],
                 person_details['diet'],
                 ))

            self.con.commit()
            return str(person_id)
        except Exception as e:
            print(e)
            self.con.rollback()
        finally:
            self._disconnect()

    def edit_person(self, person_id, **person_details):
        try:
            cur = self._connect()
            cur.execute(
                "UPDATE rsvp SET guestName = %s, email = %s,  howMany =%s , diet = %s WHERE id = %s;",
                (person_details['guest_name'],
                 person_details['email'],
                 person_details['how_many'],
                 person_details['diet'],
                 person_id))

            self.con.commit()
        except Exception as e:
            self.con.rollback()
            print(e)
        finally:
            self._disconnect()

    def remove_person(self, person_id):
        try:
            cur = self._connect()
            cur.execute("DELETE FROM rsvp WHERE id = %s;", (person_id,))
            self.con.commit()
        except Exception as e:
            print(e)
            self.con.rollback()
        finally:
            self._disconnect()
