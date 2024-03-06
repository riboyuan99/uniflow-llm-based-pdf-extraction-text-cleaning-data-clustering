import unittest
from unittest.mock import MagicMock, patch

from uniflow.flow.extract.extract_image_flow import ExtractImageFlow
from uniflow.node import Node
from uniflow.op.extract.split.constants import PARAGRAPH_SPLITTER


class TestExtractImageFlow(unittest.TestCase):
    @patch("uniflow.flow.extract.extract_image_flow.ExtractImageOp")
    @patch("uniflow.flow.extract.extract_image_flow.ProcessImageOp")
    @patch("uniflow.flow.extract.extract_image_flow.SplitterOpsFactory")
    @patch("uniflow.flow.extract.extract_image_flow.CvModel")
    def setUp(
        self,
        mock_cv_model,
        mock_splitter_ops_factory,
        mock_process_image_op,
        mock_extract_image_op,
    ):
        self.mock_extract_image_op = mock_extract_image_op
        self.mock_process_image_op = mock_process_image_op
        self.mock_splitter_ops_factory = mock_splitter_ops_factory
        self.mock_cv_model = mock_cv_model
        self.mock_cv_model.return_value = MagicMock()
        self.model_config = {"model_config": "model_config"}
        self.extract_image_flow = ExtractImageFlow(model_config=self.model_config)

    def test_init(self):
        self.mock_extract_image_op.assert_called_once_with(
            name="extract_image_op", model=self.mock_cv_model.return_value
        )
        self.mock_cv_model.assert_called_once_with(model_config=self.model_config)
        self.mock_process_image_op.assert_called_once_with(name="process_image_op")
        self.mock_splitter_ops_factory.get.assert_called_once_with(PARAGRAPH_SPLITTER)

    def test_run(self):
        # arrange
        nodes = [
            Node(name="node1", value_dict={"filename": "filepath"}),
            Node(name="node2", value_dict={"filename": "filepath"}),
        ]

        self.mock_extract_image_op.return_value.return_value = MagicMock()
        self.mock_process_image_op.return_value.return_value = MagicMock()
        self.mock_splitter_ops_factory.get.return_value.return_value = MagicMock()
        result = self.extract_image_flow.run(nodes)

        self.mock_extract_image_op.return_value.assert_called_once_with(nodes)
        self.mock_process_image_op.return_value.assert_called_once_with(
            self.mock_extract_image_op.return_value.return_value
        )
        self.mock_splitter_ops_factory.get.return_value.assert_called_once_with(
            self.mock_process_image_op.return_value.return_value
        )

        self.assertEqual(
            result, self.mock_splitter_ops_factory.get.return_value.return_value
        )


if __name__ == "__main__":
    unittest.main()
