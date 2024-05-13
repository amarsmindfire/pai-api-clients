# for ind, request_form_files in enumerate(query_string):
#     sas_token = self.get_blob_sas_token(request_form_files.file_name)
#     sas_tokens.append({
#         'page_number': ind,
#         'page_image_url': 'https://myaccount.blob.core.windows.net/pictures/profile.jpg?sv=2012-02-12&st=2009-02-09&se=2009-02-10&sr=c&sp=r&si=YWJjZGVmZw%3d%3d&sig=dD80ihBh5jfNpymO5Hg1IdiJIEvHcJpCMiCMnN%2fRnbI%3d'
#
#     })
#     # encoded_string = self.get_blob(request_form_files.file_name)
#     # encoded_string_list.append(encoded_string.decode("utf-8"))
# return sas_tokens