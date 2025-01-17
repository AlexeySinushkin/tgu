from datetime import datetime


from dao.in_memory_test_event_store import InMemoryEventStore


#class TestInMemoryEventStoreCrud(unittest.TestCase):
def test_create():
  store = InMemoryEventStore()
  image = "new-image.png"
  new_event = store.create(image)
  bell_events = store.get_events(datetime.now())
  df = bell_events[bell_events['id']==new_event.id]
  assert df.shape[0] == 1
  attached_image = store.get_images(new_event.id).iloc[0]
  assert image == attached_image.file_name
