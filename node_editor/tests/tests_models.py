from django.test import TestCase
from django.contrib.auth.models import User
from wagtail.images.tests.utils import get_test_image_file
from wagtail.images.models import Image
from wagtail.documents.models import Document

from node_editor.models import NodeCategory, Node, Workflow, NodeItem, Connection


class NodeModelsTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="pass")

        # Create test images
        image_file = get_test_image_file(filename="icon.jpg")
        self.icon_image = Image.objects.create(title="Icon Image", file=image_file)

        # Create NodeCategory
        self.category = NodeCategory.objects.create(
            name="Category 1",
            icon="fa-star",
            description="Test category",
            header_class="bg-test"
        )

        # Create Node
        self.node = Node.objects.create(
            name="Node 1",
            category=self.category,
            html_id="node1",
            type="type1",
            icon=self.icon_image,
            order=1
        )

        # Create Workflow
        self.workflow = Workflow.objects.create(
            user=self.user,
            name="Workflow 1",
            description="Test workflow"
        )

        # Create NodeItems
        self.node_item1 = NodeItem.objects.create(
            workflow=self.workflow,
            node=self.node,
            original_name="Node 1",
            original_id="nid1",
            name="Node Item 1",
            html_id="item1",
            type="type1",
            icon=self.icon_image
        )
        self.node_item2 = NodeItem.objects.create(
            workflow=self.workflow,
            node=self.node,
            parent=self.node_item1,
            original_name="Node 2",
            original_id="nid2",
            name="Node Item 2",
            html_id="item2",
            type="type2",
            icon=self.icon_image
        )

        # Create Connection
        self.connection = Connection.objects.create(
            workflow=self.workflow,
            sourceId=self.node_item1.html_id,
            targetId=self.node_item2.html_id
        )

        # Create a Document
        self.document = Document.objects.create(title=self.node_item1.html_id, file=image_file)

    def test_node_category_creation(self):
        self.assertEqual(NodeCategory.objects.count(), 1)
        self.assertEqual(str(self.category), "Category 1")

    def test_node_creation(self):
        self.assertEqual(Node.objects.count(), 1)
        self.assertEqual(str(self.node), "Node 1")
        self.assertEqual(self.node.category, self.category)

    def test_workflow_creation(self):
        self.assertEqual(Workflow.objects.count(), 1)
        self.assertEqual(str(self.workflow), "Workflow 1")
        self.assertEqual(self.workflow.user, self.user)

    def test_node_item_hierarchy(self):
        # Parent-child relationship
        self.assertEqual(self.node_item2.parent, self.node_item1)
        ancestors = self.node_item2.get_ancestors()
        self.assertIn(self.node_item1, ancestors)
        descendants = self.node_item1.get_descendants()
        self.assertIn(self.node_item2, descendants)

    def test_connection_creation(self):
        self.assertEqual(Connection.objects.count(), 1)
        self.assertEqual(str(self.connection), f"{self.node_item1.html_id} -> {self.node_item2.html_id}")

    def test_node_item_delete_removes_connections_and_documents(self):
        # Ensure connection and document exist
        self.assertEqual(Connection.objects.filter(sourceId="item1").count(), 1)
        self.assertEqual(Document.objects.filter(title="item1").count(), 1)

        # Delete NodeItem 1
        self.node_item1.delete()

        # Connections where node was source or target should be deleted
        self.assertEqual(Connection.objects.filter(sourceId="item1").count(), 0)
        self.assertEqual(Connection.objects.filter(targetId="item1").count(), 0)

        # Document with title = html_id should be deleted
        self.assertEqual(Document.objects.filter(title="item1").count(), 0)

        # NodeItem itself should be deleted
        self.assertFalse(NodeItem.objects.filter(html_id="item1").exists())

    def test_unique_html_id_constraint(self):
        with self.assertRaises(Exception):
            NodeItem.objects.create(
                workflow=self.workflow,
                node=self.node,
                original_name="Duplicate",
                original_id="nid3",
                name="Duplicate Item",
                html_id="item2",  # Duplicate html_id
                type="type3"
            )
