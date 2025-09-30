from django.urls import path

from .views import (
    NodeCategoryListCreate,
    NodeCategoryDetail,
    NodeListCreate,
    NodeDetail,
    WorkflowListCreate,
    WorkflowDetail,
    WorkflowBulkDelete,
    NodeItemListCreate,
    NodeItemDetail,
    NodeItemUpdateFormData,
    ConnectionListCreate,
    ConnectionNodeDetail,
    DownloadFile
)


urlpatterns = [
    path('node_category/', NodeCategoryListCreate.as_view()),
    path('node_category/<int:pk>/', NodeCategoryDetail.as_view()),
    path('node/', NodeListCreate.as_view()),
    path('node/<int:pk>/', NodeDetail.as_view()),
    path('', WorkflowListCreate.as_view()),
    path('<int:pk>/', WorkflowDetail.as_view()),
    path('bulk_delete/', WorkflowBulkDelete.as_view()),
    path('node_item/', NodeItemListCreate.as_view()),
    path('node_item/<int:pk>/', NodeItemDetail.as_view()),
    path('node_item/form_data/<int:pk>/', NodeItemUpdateFormData.as_view()),
    path('connection/', ConnectionListCreate.as_view()),
    path('connection/<int:pk>/', ConnectionNodeDetail.as_view()),
    path('download_file/', DownloadFile.as_view()),

]
