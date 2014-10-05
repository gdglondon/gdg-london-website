var API_KEY = "AIzaSyAB3Hxs-mqSn_DHMGechNIR3neN_7Jac_k";
var PROFILE_ID = "108855452729844077920";
var ActivityWidget;
var results;

$(function() {

	ActivityWidget = $("<ul/>").addClass("feedItems").appendTo(
			jQuery(".google-plus-widget"));

	var searchUrl = "https://www.googleapis.com/plus/v1/people/" + PROFILE_ID
			+ "/activities/public?alt=json&key=" + API_KEY;

	jQuery
			.ajax({
				url : searchUrl,
				dataType : 'jsonp',
				success : function(data) {

					results = data['items'];

					var i = 0;
					while (i < 3) {
						var post = data['items'][i];
						var postObject = post['object'];

						var node = $("<li/>");
						// var header = $("<div/>").addClass("header");

						// $("<img/>").attr("src",
						// post['actor']['image']['url']).appendTo(header);
						// var temp = $("<div/>");
						// $("<a/>").attr("href",
						// post['actor'].url).append(post['actor'].displayName).appendTo(temp);

						// temp.appendTo(header);
						// header.appendTo(node);
						// $("<div/>").addClass("clears").appendTo(header);
						// $("<div/>").addClass("clears").appendTo(node)
						if (post['verb'] == "post"
								&& postObject['content'].length > 0) {
							$("<p/>").html(postObject['content'])
									.appendTo(node);
						}

						if (post['verb'] == "share") {

							var orginalPost = $("<div/>").addClass(
									"originalPost");
							$("<img />").attr("src",
									postObject['actor']['image']['url'])
									.appendTo(orginalPost);
							var temp;
							temp = $("<div/>");
							temp.append("<a href=\""
									+ postObject['actor']['url'] + "\">"
									+ postObject['actor'].displayName + "</a>");
							temp
									.append(" <span class=\"grey\">originally shared this</span>"
											+ " <a href=\""
											+ postObject['url']
											+ "\">post</a>");
							if (postObject['content'].length > 0) {
								$("<p/>").html(postObject['content']).appendTo(
										temp);
							}
							temp.appendTo(orginalPost);
							$("<div/>").addClass("clears")
									.appendTo(orginalPost);
							orginalPost.appendTo(node);
						}

						if (postObject['attachments'] != null) {
							var attachment_counter = 0;
							while (attachment_counter < postObject['attachments'].length) {
								var isArticle = false;
								if (postObject['attachments'][attachment_counter]['objectType'] == "article") {

									var postAttachments = $("<div/>").addClass(
											"postAttachments");

									var temp = $("<div/>");
									if (postObject['attachments'].length == 2) {
										$("<img/>")
												.attr(
														"src",
														postObject['attachments'][1]['fullImage']['url'])
												.appendTo(postAttachments);
									}
									temp
											.append("<a href=\""
													+ postObject['attachments'][attachment_counter]['url']
													+ "\">"
													+ postObject['attachments'][attachment_counter]['displayName']
													+ "</a><br/>");
									temp
											.append(postObject['attachments'][attachment_counter]['content']);

									temp.appendTo(postAttachments)
									$("<div/>").addClass("clears").appendTo(
											postAttachments);
									postAttachments.appendTo(node);

								}

								if (postObject['attachments'][attachment_counter]['objectType'] == "video") {
									var postAttachments = $("<div/>").addClass(
											"postAttachments");
									postAttachments
											.append("<a class=\"youtube\" href=\""
													+ postObject['attachments'][attachment_counter]['url']
													+ "\">"
													+ postObject['attachments'][attachment_counter]['displayName']
													+ "</a><br/>");

									postAttachments
											.append("<a class=\"youtube\" href=\""
													+ postObject['attachments'][attachment_counter]['url']
													+ "\">"
													+ "<img src=\""
													+ postObject['attachments'][attachment_counter]['image']['url']
													+ "\" />" + "</a>");
									// postAttachments.append(postObject['attachments'][attachment_counter]['content']);
									postAttachments.appendTo(node);

								}

								if (postObject['attachments'][attachment_counter]['objectType'] == "photo-album") {
									var postAttachments = $("<div/>").addClass(
											"postAttachments").addClass(
											"photo-album");
									$("<a/>").addClass("albumTitle").attr("href",postObject['attachments'][attachment_counter]['url']).text(postObject['attachments'][attachment_counter]['displayName']).appendTo(postAttachments);
									
/*
									if (attachment_counter < postObject['attachments'].length) {
										
										attachment_counter++;
										while (attachment_counter < postObject['attachments'].length) {
											$("<img/>")
													.attr(
															"src",
															postObject['attachments'][attachment_counter]['image']['url'])
													.appendTo(postAttachments);
											attachment_counter++;
										}

									}
									*/
									$("<div/>").addClass("clears").appendTo(
											postAttachments);
									// postAttachments.append(postObject['attachments'][attachment_counter]['content']);
									postAttachments.appendTo(node);

								}

								attachment_counter++;
							}
						}

						var temp = $("<div/>").addClass("socialStatus");
						
						
						$(temp).append(
								"<a href=\""
								+ post['url']
								+ "\"><span>+" + postObject['plusoners'].totalItems
								+ "</span><span>"
								+ postObject['replies'].totalItems
								+ " comment(s)"
								+ "</span><span>"
								+postObject['resharers'].totalItems
								+ " reshare(s)"
								+ "</span>"
								+"</a>");
										
										
						temp.appendTo(node);
						node.appendTo(ActivityWidget);
						i++;
					}
					
					$('.container').isotope('reLayout');

				}
			});

});
