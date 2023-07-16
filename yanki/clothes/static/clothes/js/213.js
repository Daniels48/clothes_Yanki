"use strict";
window.onload = function () {
	const add = "+";
	const sub = "-";
	const del = "delete"
	const global_cart = "cart";
	const global_currency = "currency";
	const global_like = "like";
	const global_delay = 1200;

	const head_search = document.querySelector(".search__input");

	const container_search_keyup = document.querySelector(".searchsub__products");

	container_search_keyup.addEventListener("mouseover", set_settings_mouseover_for_search_keyup);
	container_search_keyup.addEventListener("mouseout", clear_settings_mouseout_for_search_keyup);


	function set_settings_mouseover_for_search_keyup(e) {
		const obj = e.target
		const element_enter = obj.closest(".searchsub__item");

		if (element_enter) {
			const cls = "_keyup_enter";
			let old_element_enter = document.querySelector(`[data-isenter="True"]`);

			if (!old_element_enter) {
				old_element_enter = head_search;
				old_element_enter.dataset.isenter = "True";
			}

			old_element_enter.classList.remove(cls);
			old_element_enter.dataset.isenter = "False";

			element_enter.dataset.isenter = "True";
			element_enter.classList.add(cls);
		}

	}

	function clear_settings_mouseout_for_search_keyup(e) {
		const n_obj = e.relatedTarget.closest(".searchsub__item");

		if (!n_obj) {
			const cls = "_keyup_enter";
			const enter_element = document.querySelector(`.${cls}`);
			enter_element.classList.remove(cls);
			enter_element.dataset.isenter = "False";
			head_search.dataset.isenter = "True";
		}
	}


	/* els.addEventListener("mouseout", (e) => {
		const obj = e.target
		console.log(obj, "out")
	}); */



	document.addEventListener("unload", function () {
		const url = window.location.href.split("?");
		if (url[1]) { this.localStorage.removeItem("filters") }
	});

	/* document.addEventListener("keyup", enter_keyup)

	async function enter_keyup(e) {
		const obj = e.target;
		if (obj.classList.contains("search__input")) { search_keyup(e) }

	} */

	head_search.addEventListener("keyup", search_keyup);


	document.addEventListener('click', (e) => {
		const cls_active_element = "_active";
		const obj = e.target;
		const active = document.querySelectorAll(`.${cls_active_element}`);
		const filter_open = document.querySelectorAll("._filter_open");
		const select = document.querySelector(".info-product__choose-box");

		const head_search = obj.closest(".search__input");

		//-----------------------------------------------------------------------------------------------------//
		const change_lang_or_currency = obj.closest('.change');
		if (change_lang_or_currency) {
			const new_value = obj.closest(".change__li");

			if (new_value) {
				const old_value = change_lang_or_currency.querySelector("button.change__btn");
				const new_data = new_value.innerText;
				const old_data = old_value.innerText;
				const span = old_value.firstElementChild.outerHTML

				old_value.innerHTML = new_data + span;
				new_value.innerText = old_data;

				change_lang_or_currency.classList.toggle(cls_active_element);

				if (get_contains_cls(change_lang_or_currency, "money")) {
					change_currency(new_data);
				}

			}
			else { change_lang_or_currency.classList.toggle(cls_active_element) }
		}

		//-----------------------------------------------------------------------------------------------------//
		const main_search = obj.closest('.search_ico');
		const burger_icon = obj.closest('.burger__icon');
		const catalog_product_add_like = obj.closest(".like_add");

		if (main_search) {
			const input = document.querySelector('.search__input'),
				parent = obj.closest('.header__lk'),
				width = window.screen.width,
				previus = parent.previousElementSibling,
				search = parent.nextElementSibling;

			parent.classList.toggle(cls_active_element);
			if (width > 992) previus.classList.toggle(cls_active_element);
			search.classList.toggle(cls_active_element);
			input.focus();
		}

		//-----------------------------------------------------------------------------------------------------//

		const search_select_category = obj.closest(".main2__sublink");

		if (search_select_category) {
			change_products_for_search(search_select_category, false, false);
		}

		//-----------------------------------------------------------------------------------------------------//
		if (burger_icon) {
			if (window.screen.width < 768) {
				const class_burgera = "_burger";
				const get_contains = (element, cls) => element.classList.contains(cls);
				if (get_contains(document.body, class_burgera)) {
					burger_icon.addEventListener("transitionend", (e) => {
						console.log(e);
					})
				}
				document.body.classList.toggle(class_burgera);
				burger_icon.classList.toggle(class_burgera);


			}
		}

		if (catalog_product_add_like) {
			e.preventDefault();
			change_like(catalog_product_add_like);

		}
		//-----------------------------------------------------------------------------------------------------//

		//-----------------------------------------------------------------------------------------------------//
		const auth_change_pass = obj.closest(".modals__li.pass");
		const auth_register = obj.closest(".modals__li.reg");
		const auth_button_next = obj.closest(".modals__submit");
		const authentification_exit_all = obj.classList.contains("modals");
		const authentification_exit_button = obj.classList.contains("modals__exit");
		const auth_open = obj.closest(".profile");
		const auth_pass_view = obj.closest(".modals__view");

		if (auth_change_pass) { aunthetification('1') }
		if (auth_register) { aunthetification('2') }
		if (auth_button_next) { e.preventDefault(); aunthetification("next", auth_button_next) }
		if (authentification_exit_all || authentification_exit_button) { aunthetification("reset") }

		if (auth_open) {
			const modals = document.querySelector(".modals");
			if (modals) { e.preventDefault(); modals.classList.add("_enter") }
		}

		if (auth_pass_view) {
			const input_pass = document.querySelector(".modals__psw");

			auth_pass_view.classList.toggle(cls_active_element);
			if (input_pass) {
				if (get_contains_cls(auth_pass_view, cls_active_element)) { input_pass.type = 'text' }
				else { input_pass.type = 'password' }
			}
		}
		//-----------------------------------------------------------------------------------------------------//

		//-----------------------------------------------------------------------------------------------------//
		const lk_choise_section = obj.closest(".lk__elem");
		const lk_histrory_change_row = obj.closest(".history-lk__row");
		const lk_change_Info = obj.closest(".person-info__button");

		if (lk_choise_section) {
			const list = document.querySelectorAll(".lk__elem");
			list.forEach(elem => elem.classList.remove("_select"));
			lk_choise_section.classList.add("_select");
		}

		if (lk_histrory_change_row) {
			lk_histrory_change_row.classList.toggle(cls_active_element);
			lk_histrory_change_row.parentNode.nextElementSibling.classList.toggle(cls_active_element);
		}

		if (lk_change_Info) {
			change_lk_data(lk_change_Info);
		}
		//-----------------------------------------------------------------------------------------------------//

		//-----------------------------------------------------------------------------------------------------//
		const product_view_details = obj.closest(".info-product__details-row");
		const product_addCart = obj.closest(".info-product__button-cart");
		const product_addFavorite = obj.closest(".info-product__button-love");
		const product_choice_size = obj.closest(".info-product__choose-box");
		const product_change_color = obj.closest(".info-product__color");

		if (product_view_details) {
			product_view_details.classList.toggle("enter");
			product_view_details.parentNode.nextElementSibling.classList.toggle("unview");
		}

		if (product_addCart) { change_cart(product_addCart, add, true) }
		if (product_addFavorite) { change_like(product_addFavorite, true) }

		if (product_choice_size) {
			const item = obj.closest(".list-size__item");
			const cls = "_enter";

			if (item) {
				const id = document.querySelector(".main-Object");
				id.dataset.id = item.dataset.id;
				id.dataset.max = item.dataset.max;
				const old = document.querySelector(".list-size__item._enter");
				const text = document.querySelector(".info-product__choose-text");
				const circle = item.querySelector(".list-size__circle");
				if (old) { old.classList.remove(cls) };
				item.classList.add(cls);

				text.parentNode.classList.add("_select");
				text.innerText = item.lastElementChild.innerText;

				circle.addEventListener("transitionend", function (e) {
					product_choice_size.classList.remove(cls);
					text.parentNode.classList.remove("_non_enter");
					const last = document.querySelector(".last__size");
					last.classList.remove("last");
				})

			} else { product_choice_size.classList.toggle(cls) }
		}

		if (product_change_color) {
			const hex = product_change_color.dataset.hex;
			const selector = "hex"
			const cls = "_down"
			const list_down = document.querySelectorAll(`[data-${selector}='${hex}']`);
			const list_hex = document.querySelectorAll(`[data-${selector}]`);
			const enter_size = document.querySelector(".list-size__item._enter");
			const text_size = document.querySelector(".info-product__choose-text");
			if (enter_size) { enter_size.classList.remove("_enter") };
			if (text_size) {
				text_size.innerText = "Выберите размер";
				text_size.parentNode.classList.remove("_select");
			}
			change_cls_for_elements(list_hex, "remove", cls)
			change_cls_for_elements(list_down, "add", cls)
		}
		//-----------------------------------------------------------------------------------------------------//

		//-----------------------------------------------------------------------------------------------------//
		const open_catalog_on_mobile = obj.closest('.main2__link');
		const open_filters_on_mobile = obj.closest(".filter__mobile");
		const open_filter_on_mobile = obj.closest(".filter__item");
		const choice__size = obj.closest(".filter__subitem.size");
		const choice__color = obj.closest(".filter__subitem.color");
		const reset_filters = obj.closest(".filter__reload");
		const sort_products = obj.closest(".filter__subitem.sort");
		const enter_filters = obj.closest(".filter__enter.filter__buttons");

		if (open_catalog_on_mobile) {
			const cls_catalog = "_catalog";
			open_catalog_on_mobile.classList.toggle(cls_catalog);
			const main2_catalog_body = document.querySelector('.main2__catalog-body');
			const main2_linkin = document.querySelector('.main2__row-linkin');
			const main2_list = document.querySelector('.main2__list');
			if (main2_catalog_body) { main2_catalog_body.classList.toggle(cls_catalog) };
			if (main2_list) main2_list.classList.toggle(cls_catalog);
			if (main2_linkin) main2_linkin.classList.toggle(cls_catalog);
		}

		if (open_filters_on_mobile) {
			open_filters_on_mobile.nextElementSibling.classList.toggle("_filtr");
			open_filters_on_mobile.lastElementChild.classList.toggle("_filtr");
		}

		if (open_filter_on_mobile) {
			const width = window.screen.width;
			const class_name = width > 767.9 ? "_filter_open" : "_filter_open";
			const list = document.querySelectorAll(`.${class_name}`);
			const buttons_wrapper = document.querySelector(".filter__buttons-wrapper");
			const filter_buttons = document.querySelector(".filter__box-buttons");
			const cls = "open_btn";

			if (list) {
				list.forEach(elem => { elem.classList.remove(class_name) })
			}

			open_filter_on_mobile.classList.toggle(class_name); //head

			if (filter_buttons) {

				const filtr_open = document.querySelectorAll(".open");
				if (!get_contains_cls(filter_buttons, cls)) { filter_buttons.classList.add(cls) }
				if (!filtr_open.length) { filter_buttons.classList.remove(cls) }
			}

			if (buttons_wrapper) {
				if (get_contains_cls(open_filter_on_mobile.parentNode, "sort")) {
					buttons_wrapper.classList.toggle(cls)
				}
			}

			if (get_contains_cls(open_filter_on_mobile, "price")) {
				open_filter_on_mobile.classList.toggle("open")
			}

		}

		if (choice__size) { choice__size.classList.toggle("choice"); input_installValue(choice__size, "size") }
		if (choice__color) { choice__color.classList.toggle("choice"); input_installValue(choice__color, "color") }


		if (enter_filters) {
			enter_and_get_url_filters();
		}
		//------------------------------------------------------------------------------------------------------//

		if (reset_filters) {
			const choices = document.querySelectorAll(".choice");
			if (choices.length) { choices.forEach(elem => elem.classList.remove("choice")) }
			sort_product('reload');
			localStorage.removeItem("filters");
			if (location.search) { location.search = "" }
		}

		if (sort_products) {
			const choice = document.querySelector('.filter__subitem.sort.choice');
			if (choice) { choice.classList.remove('choice'); }
			sort_products.classList.add("choice");
			sort_product(sort_products.dataset.id);
		}
		//-----------------------------------------------------------------------------------------------------//

		//-----------------------------------------------------------------------------------------------------//
		const cart_delete = obj.closest(".cart__delete");
		const cart_minus = obj.closest(".cart__minus");
		const cart_plus = obj.closest(".cart__plus");
		const cart_choice_delivery = obj.closest(".decoration__radio");

		if (cart_delete) { change_cart(cart_delete, del) }
		if (cart_minus) { change_cart(cart_minus, sub) }
		if (cart_plus) { change_cart(cart_plus, add) }

		if (cart_choice_delivery) {
			const box = cart_choice_delivery.closest(".decoration__box");
			const [cls1, cls2] = ["delivery", "pay"];
			const incld = cls => box.classList.contains(cls);
			if (incld(cls1)) { del_cls(cls1) };
			if (incld(cls2)) { del_cls(cls2) };

			function del_cls(cls) {
				const list = document.querySelectorAll(".decoration__radio" + "." + cls);
				list.forEach(elem => elem.classList.remove(cls));
				cart_choice_delivery.classList.add(cls);
				box.nextElementSibling.value = cart_choice_delivery.dataset.value;
			}

		}
		//-----------------------------------------------------------------------------------------------------//

		//-----------------------------------------------------------------------------------------------------//
		const footer_view_info = obj.closest(".footer_row");
		if (footer_view_info) {
			for (let item of footer_view_info.parentNode.children) item.classList.toggle(cls_active_element);
		}
		//-----------------------------------------------------------------------------------------------------//

		//-----------------------------------------------------------------------------------------------------//
		if (active.length) {
			active.forEach(elem => {
				elem.classList.remove(cls_active_element);

				if (get_contains_cls(elem, "modals__view")) {
					const input_pass = document.querySelector(".modals__psw");
					if (input_pass.type == "text") {
						input_pass.type = 'password';
					}
				}

				if (obj == head_search) {
					const list_class = ["header__lk", "header__change", "header__search"]
					if (list_class.some(check_class)) {
						elem.classList.add(cls_active_element);
					}
				}

				function check_class(element) {
					return elem.classList.contains(element);
				}
			})
		}
		//-----------------------------------------------------------------------------------------------------//

		//-----------------------------------------------------------------------------------------------------//
		if (filter_open.length) {
			filter_open.forEach(elem => {
				if (!obj.closest(".filter__subitem")) {
					elem.classList.remove("_filter_open");
				}
			})
		}//-----------------------------------------------------------------------------------------------------//

		//-----------------------------------------------------------------------------------------------------//
		if (select) {
			if (!obj.closest(".info-product__choose-box")) { select.classList.remove("_enter") }
		}

		//---------------------------------------------change_lk------------------------------------------------//
		async function change_lk_data(object) {
			e.preventDefault();
			const btn_input = object.firstElementChild;
			const request = {};


			if (btn_input.value == "ОБНОВИТЬ ИНФОРМАЦИЮ") {
				inputDisabled(true);
				const str_url = "profile/info";
				const url = get_global_url(str_url);
				const response = send_data_on_server(request, url);
				await get_data_in_promise(response, success_fnc, false_fnc)
				btn_input.value = "ИЗМЕНИТЬ ИНФОРМАЦИЮ";
			} else {
				btn_input.value = "ОБНОВИТЬ ИНФОРМАЦИЮ";
				inputDisabled(false);
			}

			function success_fnc(e) {
				console.log(e)
			}

			function false_fnc(e) {

			}

			function inputDisabled(value) {
				const inputs = document.querySelectorAll("input.info");
				if (inputs) {
					inputs.forEach(elem => {
						elem.disabled = value;
						elem.classList.toggle(cls_active_element);
						const name = elem.name;
						if (elem.value) {
							request[name] = elem.value;
						}
					});
				}
			}
		}
		//-----------------------------------------------------------------------------------------------------//


		async function change_products_for_search(obj, isEnter_filters, url_set) {
			const is_search = "search";
			const isNotEmptyFilters = window.location.href.match(/\?(.+)/);
			const head_url = window.location.href.split(`/${is_search}/`)[1];

			if (head_url && isNotEmptyFilters) {
				e.preventDefault();
				const request = get_request(obj, isEnter_filters);
				const url = get_global_url(is_search);
				const response = send_data_on_server(request, url);
				await get_data_in_promise(response, success_fnc, false_fnc)

				function success_fnc(data) {
					const products_query = data.products;
					const list_category = data.category;

					if (isEnter_filters) {
						const sum = data.sum;
						const element_sum = document.querySelector(".search__count");
						element_sum.innerText = sum;
						set_category(list_category);
					} else {
						const cls = "_search__select";
						const list_select = document.querySelectorAll(`.main2__sublink.${cls}`);
						list_select.forEach(elem => elem.classList.remove(cls))
						obj.classList.add(cls);
						set_url_no_reload(obj.href);
					}

					set_products(products_query);
				}

				function set_category(list) {
					const parent_category = document.querySelector(".main2__list");
					parent_category.innerHTML = "";
					for (let key in list) {
						const data = list[key];
						if ((data.enter && key == "Все") || data.who) {
							set_url_no_reload(data.url);
						}
						parent_category.insertAdjacentHTML("beforeEnd", get_html(key, list[key]))
					}

					function get_html(key, value) {
						const cls = (value.enter && key == "Все") || value.who ? " _search__select" : ""
						const element = `<a href="${value.url}" class="main2__sublink text-16${cls}" data-url="${value.url}">${key}
									<span class="search__cnt">(${value.count})</span>
								</a>`
						return element;
					}
				}

				function set_products(products_query) {
					const parent_products = document.querySelector(".main2__products");
					const load_image = `<div class="load">
											<div class="load__body">
												<div class="load__lds-ring">
													<div></div>
													<div></div>
													<div></div>
													<div></div>
												</div>
											</div>
										</div>`;
					parent_products.innerHTML = "";
					products_query.forEach(elem => parent_products.insertAdjacentHTML("beforeEnd", get_html(elem)));
					sort_product();
					parent_products.insertAdjacentHTML("beforeEnd", load_image);

					function get_html(elem) {
						const cls_like = elem.like ? "icon-like_n" : "icon-like_m";
						const element = `<div data-price="${elem.price}" data-like="${elem.id}" class="main2__item">
										<a a href = "${elem.url}" class="main2__img">
											<img src="${elem.image}" alt="img">
											<span class="${cls_like} like_add"></span>
										</a>
										<div class="main2__content-text">
											<a href="${elem.url}" class="main2__title text-16">${elem.title}</a>
											<div class="main2__price text-16 _price">${elem.f_price}</div>
											<div class="lds-roller">
												<div></div>
												<div></div>
												<div></div>
												<div></div>
												<div></div>
												<div></div>
												<div></div>
												<div></div>
											</div>
											<div class="main2__size size">
												<ul class="size__list">
													${get_size_list(elem.size)}
												</ul>
											</div>
											<div class="main2__color color">
												<ul class="color__list">
													${get_color_list(elem.color)}
												</ul>
											</div>
											<div class="main2__span">
												${get_tags_list(elem.tag)}
											</div>
										</div>
									</div>`;
						return element;

						function get_size_list(list_elem) {
							const html_outer = element => `<li class="size__li text-16">${element}</li>`;
							const list = [];
							list_elem.forEach(elem => list.push(html_outer(elem)))
							return list.join(" ");
						}

						function get_color_list(list_elem) {
							const html_outer = (element, style) => `<li class="color__li" style="background: ${element}${style}"></li>`;
							const list = [];
							list_elem.forEach(elem => {
								const slyle_elem = elem == "#ffffff" ? "; border: 1px solid #252525;" : "";
								list.push(html_outer(elem, slyle_elem))
							})
							return list.join(" ");
						}

						function get_tags_list(list_elem) {
							const html_outer = element => `<span class="text-16">${element}</span>`;
							const list = [];
							list_elem.forEach(elem => { list.push(html_outer(elem)) })
							return list.join(" ");
						}
					}
				}

				function false_fnc() {
				}
			}

			function get_request(obj, filters) {
				if (filters) {
					const request = {};
					for (let key in filters) {
						const value = filters[key];
						request[key] = value;
					}
					return request
				}
				const request = get_url_filters(obj)
				return request
			}
		}

		//-----------------------------------------click_function------------------------------------------------//
		function input_installValue(element, value) {
			const name_item = "filters"
			const filters = get_localItem(name_item) ? get_localItem(name_item) : {};
			if (!filters) {
				filters[value] = [element.dataset.id,];
				set_localItem(filters, name_item);
			} else {
				if (value in filters) {
					let old_value = filters[value];
					const enter_value = element.dataset.id;
					const index = old_value.indexOf(enter_value);
					if (index === -1) { old_value.push(enter_value); }
					else { old_value.splice(index, 1) }
					filters[value] = old_value;
					set_localItem(filters, name_item);
				} else { filters[value] = [element.dataset.id,]; set_localItem(filters, name_item); }

				if (filters[value].length == 0) { delete filters[value] };
				const isNotEmpty = Object.entries(filters).length !== 0;
				if (!isNotEmpty) { localStorage.removeItem(name_item) }
				else { set_localItem(filters, name_item) };
			}

		}

		function enter_and_get_url_filters() {
			e.preventDefault();
			const full_filters = get_full_filters();
			const isNotEmpty = Object.entries(full_filters).length !== 0;

			if (isNotEmpty) {
				const is_search = "/search/";
				const head_url = window.location.href.split(is_search)[1];

				if (head_url) {
					const list_filters = get_filtered_filters(full_filters);
					const string_added_filters = get_string_filters(list_filters) == "" ? "" : "&" + get_string_filters(list_filters);
					change_products_for_search(false, get_full_filters(), string_added_filters);

				} else {
					const string_filters = get_string_filters(get_full_filters());
					const string_query = `?${string_filters}`;
					change_url(string_query);
				}
			}


			function get_full_filters() {
				const name_item = "filters";
				const min = document.querySelector(".input-min");
				const max = document.querySelector(".input-max");
				const filters = get_localItem(name_item) ? get_localItem(name_item) : {};
				const max_price = get_localItem("max_price");

				if (parseInt(min.value) != 0) { filters["min"] = parseInt(min.value) }
				else { delete filters["min"] };
				if (parseInt(max.value) != max_price) { filters["max"] = parseInt(max.value) }
				else { delete filters["max"] };

				set_localItem(filters, name_item);

				return filters;
			}

			function get_filtered_filters(obj) {
				const list_filters = obj;
				delete list_filters["query"];
				delete list_filters["category"];
				return list_filters;
			}

			function get_string_filters(obj) {
				const list_query = [];
				for (let key in obj) {
					const value = ["min", "max"].indexOf(key) == -1 ? obj[key].join(",") : obj[key];
					list_query.push(`${key}=${value}`);
				}
				return list_query.join("&")
			}

			function change_url(list_filters) {
				window.location.href = list_filters;
			}

		}
	});

	async function search_keyup(e) {
		const inp_value = head_search.value;
		const cls_unview = "unview"
		const cls = "searchsub__item";
		const element_search = document.querySelector(`.${cls}s`);
		const element_products = element_search.firstElementChild;
		const element_category = element_search.lastElementChild;
		const window_width = window.screen.width;


		const key = e.key;
		const list_key = ["ArrowDown", "ArrowUp"];
		const list_tabs = document.querySelectorAll("[data-index]");

		if (list_key.includes(key) && list_tabs.length) {
			let element_enter = document.querySelector(`[data-isenter="True"]`)

			if (!element_enter) {
				element_enter = head_search;
				element_enter.dataset.isenter = "True";
			}


			const index = element_enter.dataset.index;

			if (list_key[0] == key) {
				const next_index = Number(index) + 1;
				let next_element = document.querySelector(`[data-index="${next_index}"]`)
				if (!next_element) { next_element = head_search }
				set_settings(next_element);

			} else {
				const prev_index = Number(index) - 1;
				const max_index = head_search.dataset.max_index;
				let prev_element = document.querySelector(`[data-index="${prev_index}"]`)
				if (!prev_element) { prev_element = document.querySelector(`[data-index="${max_index}"]`) }
				set_settings(prev_element);
			}

			function set_settings(element) {
				const cls = "_keyup_enter";
				const value_input = element.dataset.input;
				head_search.value = value_input;

				element_enter.dataset.isenter = "False";
				element_enter.classList.remove(cls);

				if (element != head_search) {
					element.classList.add(cls);
				}

				element.dataset.isenter = "True";
			}
		} else {
			if (inp_value) {
				const url = get_global_url('search');
				const request = {};
				request["keyup_search"] = inp_value;
				const response = send_data_on_server(request, url);
				await get_data_in_promise(response, true_response, false_response)
			} else {
				clear__elements();
				unview_elements("add");
			}
		}


		function true_response(raw_data) {
			clear__elements();
			const products = raw_data.products;
			const enter_value = raw_data.enter_value;
			const max_index = raw_data.max_index;
			head_search.dataset.index = 0;
			head_search.dataset.input = enter_value;
			head_search.dataset.max_index = max_index;

			if (products.length) {
				unview_elements("remove");
				append_elements(products, element_products);
				const category = raw_data.category;
				append_elements(category, element_category);
			} else { unview_elements("add") }
		}

		function false_response(e) {
		}

		function unview_elements(method) {
			if (window_width > 767) { element_search.parentNode.parentNode.classList[method](cls_unview) }
			else {
				const antimethod = method == "add" ? "remove" : "add";
				element_search.classList[method](cls_unview); document.querySelector(".burger__items").classList[antimethod](cls_unview);
			}
		}

		function append_elements(list_objects, destination) {
			list_objects.forEach(elem => { destination.insertAdjacentHTML("beforeEnd", get_html_elements(elem)) })
		}

		function get_html_elements(elem) {
			if (elem.img) {
				return `<a href="${elem.url}" data-category="${elem.id}" class="searchsub__category">
										<div class="searchsub__textcategory">
											<div class="searchsub__title text-20">${elem.title}</div>
											<div class="searchsub__subtitle">Категория</div>
										</div>
										<div class="searchsub__img">
											<img src="${elem.img}" alt="image">
										</div>
									</a>`;
			} else {
				return `<a href='${elem.url}' data-products='${elem.id}' class="${cls}" data-index="${elem.index}" data-isenter="False" data-input="${elem.input}">
										<div class="searchsub__subitem">
											<div class="searchsub__icon icon-search"></div>
											<div class="searchsub__text">${elem.title}</div>
										</div>
								</a>`;
			}
		}

		function clear__elements() {
			element_products.innerText = "";
			element_category.innerText = "";
		}
	}

	//-------------------------------------------authenticate-------------------------------------------------//
	async function aunthetification(type, button_next = false) {
		const cls = "unview";
		if (type != "reset") {
			const raw_url = "authenticate";
			const url = get_global_url(raw_url);
			const method_local = button_next ? button_next.parentNode.dataset.type : type;
			const request = { "type": method_local };
			const time_after_reg_or_chge_pass = 3000;

			if (button_next) {
				const text_error_fields = "Не заполнено одно или несколько полей!";
				const text_error_email = "Некорректный email!";
				const login = document.querySelector(".modals__inpt.modals__item");
				const password = document.querySelector(".modals__input.modals__psw.modals__item");

				if (!ValidField(login) && !ValidField(password, true)) {
					set_error_data(text_error_fields);
					return false
				}

				if (method_local == "11" || method_local == "21") {
					const EMAIL_REGEXP = /^(([^<>()[\].,;:\s@"]+(\.[^<>()[\].,;:\s@"]+)*)|(".+"))@(([^<>()[\].,;:\s@"]+\.)+[^<>()[\].,;:\s@"]{2,})$/iu;
					const isEmailValid = email => EMAIL_REGEXP.test(email);
					if (!isEmailValid(login.value)) {
						set_error_data(text_error_email);
						return false
					}
				}

				request["login"] = login.value;
				request["password"] = password.value;

				function ValidField(item, pass = false) {
					const vals = pass ? item.parentNode : item;
					if (!vals.value) { return false };
					return vals.value.length >= 4 && !vals.classList.contains(cls);
				}

				function set_error_data(str) {
					const error = document.querySelector(".modals__error");
					error.classList.remove(cls);
					error.innerText = str;
				}
			}

			const response = send_data_on_server(request, url);
			get_data_in_promise(response, receive_data, error_receive);

			function receive_data(response) {
				const data = response.data;
				if (data != 0) {
					for (let item in data) {
						for (let vals in data[item]) {
							const method = vals;
							const value = data[item][vals];
							methods_data(method, item, value);
						}
					}
				}

				if (response.success == "yes") { window.location.reload(true) }

				function methods_data(method, elem, vals) {
					elem = elem == "pass" & (method == "placeholder" || method == "value") ? "first" : elem;
					const items = get_modals_item();

					if (method == "text") { items[elem].innerText = vals };
					if (method == "del") { items[elem].classList.remove(vals) };
					if (method == "add") { items[elem].classList.add(vals) };
					if (method == "value") { items[elem].value = vals };
					if (method == "placeholder") { items[elem].placeholder = vals };
					if (method == "type") { items[elem].parentNode.dataset.type = vals };
					if (method == "time") { setTimeout(() => { window.location.reload(true) }, time_after_reg_or_chge_pass); }
				}

			}

			function error_receive(response) { }
		} else {
			const modals = document.querySelector(".modals");
			if (modals) {
				modals.classList.remove("_enter");
				const items = get_modals_item();
				items["title"].innerText = "Авторизация";
				items["title"].classList.remove(cls, "modals__margin",);
				items["text"].classList.remove("modals__margin", "modals__none");
				items["text"].classList.add(cls);
				items["text"].value = "";
				items["email"].classList.remove(cls);
				items["email"].placeholder = "Ваш e-mail*";
				items["email"].value = "";
				items["pass"].classList.remove(cls);
				items["first"].placeholder = "Ваш пароль*";
				items["first"].value = "";
				items["ul"].classList.remove(cls);
				items["button"].classList.remove(cls);
				items["button"].value = "ВОЙТИ";
				items["error"].value = "";
				items["error"].classList.add(cls);
				items["title"].parentNode.dataset.type = "0";
			}
		}

		function get_modals_item() {
			const items = {}
			items["title"] = document.querySelector(".modals__title");
			items["text"] = document.querySelector(".modals__text");
			items["email"] = document.querySelector(".modals__inpt.modals__item");
			items["pass"] = document.querySelector(".modals__pass");
			items["ul"] = document.querySelector(".modals__ul");
			items["button"] = document.querySelector(".modals__submit");
			items["first"] = document.querySelector(".modals__input.modals__psw.modals__item");
			items["error"] = document.querySelector(".modals__error");
			return items
		}
	}
	//-----------------------------------------------------------------------------------------------------//

	//--------------------------------------------------cart-------------------------------------------------//
	async function change_cart(button, sign, where_change = false) {
		const [cart_products, cart_count, cart_null] = ["products", "count", "Null"];
		const [change_cart, response_command] = ["change_cart", "command"];
		const [regexp_int, regexp_max] = [/\d+/g, /\d+M/g];
		const max_product = "Max";
		const url = get_global_url(global_cart);
		const bool = where_change ? "0" : "1";
		const set_request = (id, sign) => { return { "id": id, "sign": sign, "get_currency": bool } };


		if (where_change) {
			const lst_cls = {
				"nent": "_non_enter", "nsel": "non_select", "hld": "hold",
				"ab": "animation_button", "lst": "last", "fz": "fsize"
			};
			const text_choose_size = document.querySelector(".info-product__choose-text");
			const border_text = text_choose_size.parentNode;

			if (text_choose_size.innerText == "Выберите размер") {
				border_add_cls();
				after_animation_border(false);
			} else {
				change_block_button(button, true);
				const id = String(document.querySelector("[data-id]").dataset.id);
				const request = set_request(id, sign);
				await others_func_for_send_and_receive_data(request, url, response_success, response_fail)

				function response_success(data) {
					const command = data[response_command];
					const raw_cart = data[change_cart];
					const count_in_cart = raw_cart[cart_count];
					const [validate, value] = get_validate_count(id, sign, command);

					if (!validate) {

						if (value == 0) {
						}

						if (value == max_product) {
							const last_size = document.querySelector(".last__size");
							border_add_cls();
							last_size.classList.add(lst_cls["lst"], lst_cls["fz"]);
							after_animation_border(last_size)
						}
					}
					change_block_button(button, false, raw_cart, count_in_cart);
				}

				function response_fail(data) {
				}

				function change_block_button(button, forward, raw_cart = false, count_in_cart = false) {
					button.classList.add(lst_cls["hld"], lst_cls["ab"]);
					button.disable = true;
					if (!forward) {
						button.classList.remove(lst_cls["hld"], lst_cls["ab"]);
						button.addEventListener("transitionend", () => {
							final_set_data(raw_cart, count_in_cart);
							button.disabled = false;
						});
					}
				}
			}

			function after_animation_border(max) {
				const list_elem = max ? [border_text, max] : [border_text];
				border_text.addEventListener("transitionend", () => {
					list_elem.forEach(elem => elem.classList.remove(lst_cls["nsel"], lst_cls["fz"]))
				});
			}

			function border_add_cls() {
				border_text.classList.add(lst_cls["nent"], lst_cls["nsel"]);
			}


		} else {
			change_block(button, 0, true);
			const id = get_element(button, "id");
			set_currency(false, false, id);
			const request = set_request(id, sign);
			let count_product = 0;
			await others_func_for_send_and_receive_data(request, url, response_true, response_false);

			function response_true(data) {
				const command = data[response_command];
				const raw_cart = data[change_cart];
				const count_in_cart = raw_cart != cart_null ? raw_cart[cart_count] : 0;
				const currency = data[global_currency];

				if (command != del) {
					const [validate, value] = get_validate_count(id, sign, command);

					if (validate) {
						let number = value;
						const max = get_data_in_str(value, regexp_max) ? true : false;
						if (max) { number = get_data_in_str(value, regexp_int)[0] }
						else { }

						set_count_on_listen(button, sign, number)

						function set_count_on_listen(button, sign, value) {
							const item = get_element(button, sign);
							item.innerText = value;
						}

					} else { }
					count_product = value;
				} else {
					if (raw_cart != cart_null) { }
					else {
						const element = document.querySelector(".cart__wrapper");
						element.innerHTML = data["None_cart"];
					}
					get_element(button).remove();
				}

				change_block(button, count_product);
				final_set_data(raw_cart, count_in_cart);
				set_currency(currency, true);
			}

			function response_false(data) {
				console.log(data, 424)
			}

			function change_block(element, cnt, all = false) {
				const cls = "non_enter";
				const obj = get_element(element, "+");
				const minus = obj.previousElementSibling;
				const plus = obj.nextElementSibling;
				const btn_del = get_element(element, del);

				if (all) {
					disable(minus, true);
					disable(plus, true)
					disable(btn_del, true)
				} else {
					const block = get_data_in_str(cnt, regexp_max);
					const count = Number(get_data_in_str(cnt, regexp_int)[0]);
					if (count != 0) {
						if (count > 1) { disable(minus, false) };
						if (count == 1) { disable(minus, true) };
					}
					if (block) { disable(plus, true) };
					if (!block) { disable(plus, false) };
					if (btn_del) { disable(btn_del, false) };
				}

				function disable(element, add) {
					if (add) {
						element.classList.add(cls);
						element.disabled = true;
					}
					else {
						element.classList.remove(cls);
						element.disabled = false;
					}
				}
			}
		}

		function get_validate_count(id, sign, new_value) {
			const full_data_cart = get_localItem(global_cart);
			if (full_data_cart) {
				const list_products = full_data_cart[cart_products];
				if (String(new_value) == String(list_products[id])) {
					return [false, max_product]
				}
				if (new_value == 0) {
					return [false, new_value]
				}
				if (sign != del) {
					const value = sign == add ? +1 : -1;
					const old_count = Number(get_data_in_str(list_products[id], regexp_int));
					const count_in_bd = Number(get_data_in_str(new_value, regexp_int));
					const valid_operation = old_count + value == count_in_bd;
					return [valid_operation, new_value];
				}
			} else {
				return [new_value == 1, new_value]
			}

		}

		function get_element(element, btn = false) {
			const parent = element.closest(".cart__item");
			const get_obj = selector => parent.querySelector(selector);
			if (btn == sub || btn == add) { return get_obj(".cart__count").children[1] };
			if (btn == "id") { return parent.dataset.id };
			if (btn == "max") { return parent.dataset.max };
			if (btn == del) { return get_obj(".cart__delete") };
			if (!btn) { return parent };
		}

		function final_set_data(cart, count) {
			if (cart == "Null") { localStorage.removeItem(global_cart) }
			else { set_localItem(cart, global_cart) };
			change_cart_page(count);

			function change_cart_page(count) {
				const cart = document.querySelector(".header__item.icon-cart.cart");
				const span = cart.firstElementChild;

				if (count > 0) {
					if (span) {
						const value = Number(count)
						span.innerText = value;
					} else { cart.insertAdjacentHTML("afterbegin", `<span>${Number(1)}</span>`); }
				} else {
					if (span) { span.remove() }
				}
			}
		}
	}
	//-----------------------------------------------------------------------------------------------------//

	//---------------------------------------------sort_product--------------------------------------------//
	function sort_product(method = false) {
		const list_products = document.querySelectorAll('.main2__item');
		const sorted = document.querySelector(".filter__title");
		const selector_sort = 'sort';
		const selector_old_position = 'old_position';
		const selector_new = "new";
		const time_animation = 700;

		if (list_products.length && sorted) {

			if (method) {
				const cls = "_filter_open";
				const list = document.querySelectorAll(`.${cls}`);
				list.forEach(elem => elem.classList.remove(cls));
				const products = Array.from(list_products);

				if (method == 'upprice') { moving_elements(products, false, false, false) }
				if (method == 'lowprice') { moving_elements(products, true, false, false) }
				if (method == 'new') { moving_elements(products, true, false, true) }
				if (method == 'reload') { /* moving_elements(products, false, true, false) */reload_current_page() }

			} else { install__dataProduct(list_products) }


			function change_loading_image() {
				const load = document.querySelector(".load");
				load.classList.toggle(selector_sort);
				setTimeout(() => {
					products.forEach(element => { element.parentNode.append(element) })
					load.classList.toggle(selector_sort);
				}, time_animation)
			}

			function moving_elements(products, lower = false, old_position = false, new_s) {
				const load = document.querySelector(".load");
				sort_elements(products, lower, old_position, new_s);
				load.classList.toggle(selector_sort);
				setTimeout(() => {
					products.forEach(element => { element.parentNode.append(element) })
					load.classList.toggle(selector_sort);
				}, time_animation)

				function sort_elements(list_elements, lower = false, old_position = false, new_s) {
					list_elements.sort((a, b) => {
						let x = old_position ? get_old_parametrs(a) : get_new_parametrs(a, new_s)[0];
						let y = old_position ? get_old_parametrs(b) : get_new_parametrs(b, new_s)[0];
						if (x == "first" && y == 'last') { return -1 }
						if (x == "last" && y == 'first') { return 1 }
						if (x == "first" && y != 'first' && y != 'last') { return -1 }
						if (x == "last" && y != 'first' && y != 'last') { return 1 }
						return x - y
					})

					if (lower) list_elements.reverse();
				}

				function get_new_parametrs(element, new_s = false) {
					if (new_s) { return element.dataset[selector_new] }
					return element.dataset[selector_sort].split(",")
				}

				function get_old_parametrs(element) { return element.dataset[selector_old_position] }
			}

			function install__dataProduct(list_products) {
				list_products.forEach(element => {
					add_old_position(element);
					install_dataElements(element);
				})

				function add_old_position(element) {
					element.dataset[selector_old_position] = get_old_position(element);

					function get_old_position(element) {
						const list = Array.from(element.parentNode.children);
						const position = list.indexOf(element);
						if (position == '0') { return "first" }
						if (position == list.length - 1) { return "last" }
						return position
					}
				}

				function install_dataElements(element) {
					const spans = Array.from(element.querySelector(".main2__span").children);
					if (spans.length) {
						let New = 0
						spans.forEach(elem => { if (elem.innerText == "New") { New = 1 } })
						element.dataset[selector_new] = New;
					}

					element.dataset[selector_sort] = [get_priceElement(element)]

					function get_priceElement(element) {
						const rowContent = element.lastElementChild.children[1].textContent;
						return /\d+[.,]?(\d{2})?/.exec(rowContent)[0]
					}
				}
			}

			function reload_current_page() { window.location.href = location.protocol + '//' + location.host + location.pathname; }
		}
	}
	//-----------------------------------------------------------------------------------------------------//

	//--------------------------------------------set_currency---------------------------------------------//
	async function change_currency(value) {
		set_currency(false, false, 0);
		const url = get_global_url(global_currency);
		const request = set_request(value);
		const response = send_data_on_server(request, url);
		await timeout(response, yes, no)

		function yes(data) { set_currency(data) }
		function no(data) { }

		function set_request(value) {
			const request = { local: "True" }
			request[global_currency] = value;
			return request
		}
	}

	function set_currency(data = false, cart = false, add = false) {
		const selector_sum_cart = "cart__itog-sum";
		const selector_product = "[data-price]";
		const cls_sum = "_itog";
		const [cls_price, cls_unview, cls_add] = ["_price", "unview", "_currency"];
		const get_one_element_on_id = id => document.querySelector(`[data-id='${id}']`);
		const get_element = element => element.querySelector(`.${cls_price}`);

		if (!(add === false)) { change_elements_cls(add) }

		if (data) {
			const get_finally_value = (value, sign) => `${value} ${sign}`;

			try {
				const max_range_value = Number(data.data.max_price);
				set_localItem(max_range_value, "max_price");
				const url = window.location.href;
				const start = url.match(/min=(\d+)/) ? url.match(/min=(\d+)/)[1] : 0;
				const finsih = url.match(/max=(\d+)/) ? url.match(/max=(\d+)/)[1] : max_range_value;
				change_slider(start, finsih, max_range_value);
			} catch { }


			if (cart) {
				const sum_cart = data["sum_cart"];
				const product_data = data["product"];
				const id_product = product_data["id"];
				const sum_product = product_data["sum"];
				const local_sign = product_data["sign"];

				if (sum_product > 0) {
					const element = get_one_element_on_id(id_product);
					get_animation(animation_product, element, local_sign)

				} if (sum_cart > 0) {
					const element = document.querySelector(`.${selector_sum_cart}`);
					get_animation(animation_product, element, local_sign)
				}

				function animation_product(first, element, sign) {
					const valid_all_sum = element.classList.contains(selector_sum_cart);
					const value = valid_all_sum ? sum_cart : sum_product;
					change_cls_for_animate(element);
					const text = valid_all_sum ? element : get_element(element)
					if (first) { set_price_for_product(text, value, sign) };
				}

			} else {
				const [local_var, sign_var, old_c, new_c] = ["local", "sign", "old", "new"];
				const default_currency = "UAH";
				const count_round = 2;
				const currency = data[local_var];
				const dates = data["data"];
				const [old_value, new_value, sign] = [dates[old_c], dates[new_c], dates[sign_var]];
				const get_value = elem => Number(elem.querySelector(".cart__count").children[1].innerText);


				const list = document.querySelectorAll(selector_product);
				if (list.length) {
					list.forEach(elem => {
						if (get_contains_cls(elem, "cart__item")) {
							get_animation(action_product, elem, "*")
						} else {
							get_animation(action_product, elem)
						}
					});
				}

				const dbl_slider = document.querySelectorAll(".range-slider__money");
				if (dbl_slider.length) {
					dbl_slider.forEach(elem => { elem.innerText = sign })
				}

				const cart_itog = document.querySelector(`.${selector_sum_cart}`);
				if (cart_itog) {
					let sum = 0;
					const list_cart = document.querySelectorAll(`.${cls_price}`);
					const get_value = text => Number(text.innerText.match(/\d+\.?\d+/)[0]);
					list_cart.forEach(elem => sum += get_value(elem));
					sum = Math.round(sum * +`1e${count_round}`) / +`1e${count_round}`;
					change_cls_for_animate(cart_itog);
					set_price_for_product(cart_itog, sum, sign)
				}

				set_localItem(currency, global_currency);

				function action_product(first, element, sign) {
					const action = sign ? [element, sign, get_value(element)] : [element];
					change_cls_for_animate(element);
					if (first) { set_price(...action) }
				}

				function set_price(element, vars = false, val = 1) {
					const row_price = Math.round(Number(element.dataset.price.replace(",", ".")));
					const number = row_price * val;
					const new_price = number => Math.round(
						(row_price * old_value) * number / new_value * +`1e${count_round}`
					) / +`1e${count_round}`;
					let final_value = currency == default_currency ? row_price : new_price(1);
					if (vars == "*") { final_value = currency == default_currency ? number : new_price(get_value(element)) };
					return set_price_for_product(get_element(element), final_value, sign)
				}
			}

			function get_animation(func, element = false, sign = false) {
				func(true, element, sign);
			}

			function set_price_for_product(element, value, sign) {
				element.innerText = get_finally_value(value, sign);
				return element
			}
		}

		function change_elements_cls(id) {
			const elements = id == 0 ? document.querySelectorAll(selector_product) : [get_one_element_on_id(id)];
			if (elements.length) {
				elements.forEach(elem => {
					change_cls_for_animate(elem)
				});
			}
			const sum_element = document.querySelector(`.${selector_sum_cart}`);
			if (sum_element) {
				change_cls_for_animate(sum_element);
			}
		}

		function change_cls_for_animate(head_element) {
			const valid_all_sum = head_element.classList.contains(selector_sum_cart);
			const element = valid_all_sum ? head_element : get_element(head_element);
			const anim = element.nextElementSibling ? element.nextElementSibling : element.parentNode.nextElementSibling;
			if (valid_all_sum) {
				element.classList.toggle(cls_sum);
				element.previousElementSibling.classList.toggle(cls_sum);
			} else { element.classList.toggle(cls_unview); }
			anim.classList.toggle(cls_add);
		}
	}
	//-----------------------------------------------------------------------------------------------------//

	//--------------------------------------------set_like--------------------------------------------------//
	async function change_like(button, lst_product = false) {
		const [cls_out, cls_in] = ["icon-like_m", "icon-like_n"];
		const selector_object = lst_product ? "main-Object" : "main2__item";
		const id_product = button.closest(`.${selector_object}`).dataset.like;
		const url = get_global_url(global_like);
		const where_add = lst_product ? 1 : 0;
		const icon = lst_product ? button.querySelector(".info-product__icon-love") : button;
		const sign_request = get_sign_operation(icon);
		const request = { "local": "True" };
		request[global_like] = { "id": id_product, "sign": sign_request, "where_add": where_add };


		const response = send_data_on_server(request, url);
		get_data_in_promise(response, sucs_true, sucs_false);


		function sucs_true(data) {
			const like_data = data[global_like];
			const command = like_data["command"];
			const local_list_like = like_data["list_like"];
			const sign_response = like_data["sign"];
			const where_add = like_data["where_add"];

			if (command == "true") {
				if (where_add == 1) {
					const element_text = button.querySelector(".info-product__button-love-text");
					const text = get_include_cls(icon) ? "В ИЗБРАННОМ" : "В ИЗБРАННОЕ";
					element_text.innerText = text;
				}
				change_cls_like(icon, sign_response);
			} else {

			}
			if (local_list_like.length == 0) { localStorage.removeItem(global_like) }
			else { set_localItem(local_list_like, global_like) }

		}

		function sucs_false(data) {

		}

		function change_cls_like(button, sign) {
			if (sign == add) {
				button.classList.remove(cls_out);
				button.classList.add(cls_in);
			} else {
				button.classList.remove(cls_in);
				button.classList.add(cls_out);
			}
		}

		function get_sign_operation(element) {
			const valid = get_include_cls(element);
			return valid ? add : del
		}

		function get_include_cls(element) {
			return element.classList.contains(cls_out)
		}
	}
	//-----------------------------------------------------------------------------------------------------//

	//--------------------------------------------general--------------------------------------------------//
	function general() {
		//-----------------------------------------dinamic_adaptiv---------------------------------------------//
		function dinamicAdaptiv() {
			// data-da="1,2,3,4,5,6"
			//1(required) - destination (class_list, id) //example "asd ddd" or #fsf413313
			//2(required) - place (first, other int, last)//3(required) - width (width) //example 1210
			//4(non required) - class_delete (class_list)//5(non required) - class_add (class_list)
			//6(non required) - class_contains elements click (when you click)//7(non required) - class contains(when you click)
			const selector_search = "da";
			const types = "max"; //max or min;
			const selector_old_position = 'old';
			//---------------------------------------------------------------------------------------------//
			const list_objects = Array.from(document.querySelectorAll(`[data-${selector_search}]`));
			const list_points_media = {};
			const list_width = [];
			//---------------------------------------------------------------------------------------------//

			if (list_objects.length) {
				list_objects.forEach(element => {
					add_old_parametrs(element);
					add_point_media(element);
					add_check_change(element);

					function add_point_media(element) {
						const name = `width_${get_width(element)}`;
						if (name in list_points_media) { list_points_media[name].push(element); }
						else { list_points_media[name] = []; list_points_media[name].push(element); }
					}

					function add_check_change(element) {
						const point = get_width(element);
						const method = "addEventListener";
						if (list_width.indexOf(point) == -1) {
							list_width.push(point);
							get_matchMedia(point)[method]('change', change_breakpoint);
						}
					}

					function add_old_parametrs(element) {

						function get_old_position(element) {
							const list = Array.from(element.parentNode.children);
							const position = list.indexOf(element);
							if (position == '0') { return "first" };
							if (position == list.length - 1) { return "last" };
							return position
						}

						function get_old_parent(element) {
							if (!element.parentNode.id) {
								const random = String(Math.round(((Math.random() + 0.01) * 1000000000)));
								element.parentNode.id = random;
							}
							return element.parentNode.id
						}

						element.dataset[selector_old_position] = [get_old_parent(element), get_old_position(element)].join(",");
					}

					function get_width(element) { return get_new_parametrs(element)[2] }
				})

				list_width.forEach(element => {
					if (get_matchMedia(element).matches) {
						const list = list_points_media[`width_${element}`];
						sort_elements(list, true);
						replace_positions(list, true);
					}
				})

				function get_matchMedia(width) { return window.matchMedia(`(${types}-width: ${width}px)`) }

				function replace_positions(list, forward = true) {
					list.forEach(element => {
						const [station, place, width, remove_class, add_class, element_click, class_click] = get_new_parametrs(element);

						if (forward) {
							if (element_click) { check_button(new_position, old_position); }
							else { new_position(); }
						}

						else {
							if (element_click) { check_button(new_position, old_position); }
							else { old_position(); }
						}

						function new_position() {
							moving_element(get_station(station, element), place, element);
							append_class(element, add_class);
							delete_class(element, remove_class);
						}

						function old_position() {
							const [station, place] = get_old_parametrs(element);
							moving_element(get_station("#" + station), place, element);
							append_class(element, remove_class);
							delete_class(element, add_class);
						}

						function check_button(new_position, old_position) {
							const button = get_station(element_click);
							if (button) {
								const mutationObserver = new MutationObserver(get_mutation);
								mutationObserver.observe(document.body, { attributes: true, subtree: true });

								function get_mutation(mutation) {
									if (button.classList.contains(class_click)) { new_position(); }
									else { old_position(); }
								}
							}
						}

						function get_station(selector, element = false) {
							if (selector) {
								if (/^\s*!/.test(selector)) {
									const parent = selector.match(/(?<=!\s*)(?=\s*)([\w-]\s*)+/g)[0].replace(/\s+/g, ".");
									const obj = selector.match(/(?<=;\s*)(?=\s*)[\w-]+/g)[0].replace(/\s+/g, ".");
									return element.closest("." + parent).querySelector("." + obj);
								}
								if (/^\s?#/.test(selector)) {
									const id = selector.match(/(?<=#\s*)(?=\s*)[_\w-]+/)[0];
									if (id) { return document.getElementById(id) }
								} else {
									const class_list = selector.match(/[\w-]+/g).join(".");
									if (class_list) { return document.querySelector("." + class_list) }
								}
							}
						}

						function moving_element(parent, place, element) {
							if (place == 'last') { parent.append(element) }
							else if (place == 'first') { parent.prepend(element) }
							else { parent.children[place - 1].after(element) }
						}

						function delete_class(element, class_list) {
							if (class_list) {
								const list = class_list.split(" ");
								list.forEach(item => { if (element.classList.contains(item)) element.classList.remove(item) })
							}
						}

						function append_class(element, class_list) {
							if (class_list) {
								const list = class_list.split(" ");
								list.forEach(item => { if (!element.classList.contains(item)) element.classList.add(item) })
							}
						}
					})
				}

				function change_breakpoint(breakpoint) {
					const mediaWidth = breakpoint.media.match(/\d+\.?\d+/)[0];
					const list = list_points_media[`width_${mediaWidth}`];

					if (breakpoint.matches) {
						sort_elements(list, true);
						replace_positions(list, true);
					} else {
						sort_elements(list, true);
						replace_positions(list, false);
					}
				}

				function sort_elements(list_elements, old_position = false) {
					list_elements.sort((a, b) => {
						const x = old_position ? get_old_parametrs(a)[1] : get_new_parametrs(a)[1];
						const y = old_position ? get_old_parametrs(b)[1] : get_new_parametrs(b)[1];
						if (x == "first" && y == 'last') { return -1 };
						if (x == "last" && y == 'first') { return 1 };
						if (x == "first" && y != 'first' && y != 'last') { return -1 };
						if (x == "last" && y != 'first' && y != 'last') { return 1 };
						return x - y
					})
				}

				function get_new_parametrs(element) { return element.dataset[selector_search].split(",") }

				function get_old_parametrs(element) { return element.dataset[selector_old_position].split(",") }
			}
		}
		//-----------------------------------------GallertSlider-----------------------------------------------//
		function GallerySlider() {
			const BoxSlider = document.querySelector(".category__box");
			if (BoxSlider) {
				$(document).ready(function () {
					$('.category__box').slick({
						slidesToShow: 3, slidesToScroll: 1,
						responsive: [{ breakpoint: 992, settings: { slidesToShow: 2, slidesToScroll: 1, } },
						{ breakpoint: 375, settings: { slidesToShow: 1, slidesToScroll: 1 } }
						]
					})
				})
			}
		}
		//-----------------------------------------RangeSlider-----------------------------------------------//
		function RangeSlider() {
			const rangeSlider = document.querySelector(".range-slider__range");
			const rangeMin = document.querySelector(".input-min");
			const rangeMax = document.querySelector(".input-max");
			const rangeInputs = [rangeMin, rangeMax];
			if (rangeSlider || rangeMin || rangeMax) {
				const max_range_value = Number(rangeMax.dataset.value);
				set_localItem(max_range_value, "max_price");
				noUiSlider.create(rangeSlider, { // инициализируем слайдер
					start: [0, max_range_value], // устанавливаем начальные значения
					connect: true, // указываем что нужно показывать выбранный диапазон
					padding: [0, 0],
					range: { // устанавливаем минимальное и максимальное значения
						'min': [0],
						'max': [max_range_value]
					},
					step: 1, // шаг изменения значений
				})
				rangeSlider.noUiSlider.on('update', function (values, handle) { // при изменений положения элементов управления слайдера изменяем соответствующие значения
					rangeInputs[handle].value = parseInt(values[handle]);
				});
				rangeMin.addEventListener('change', function () { // при изменении меньшего значения в input - меняем положение соответствующего элемента управления
					rangeSlider.noUiSlider.set([this.value, null]);
				});
				rangeMax.addEventListener('change', function () { // при изменении большего значения в input - меняем положение соответствующего элемента управления
					rangeSlider.noUiSlider.set([null, this.value]);
				});

			}
		}
		dinamicAdaptiv();
		GallerySlider();
		RangeSlider();
	}
	//------------------------------------------------------------------------------------------------------//

	//-------------------------------------------general_operation------------------------------------------//
	function get_contains_cls(element, cls) {
		return element.classList.contains(cls)
	}

	function get_data_in_str(str, regexp) {
		return String(str).match(regexp);
	}

	function change_cls_for_elements(list, method, cls) { list.forEach(elem => elem.classList[method](cls)) };
	//------------------------------------------------------------------------------------------------------//

	//----------------------------------------send_and_receive_data_on_server-------------------------------//
	async function send_data_on_server(obj, url = "/") {
		const response = await fetch(url, {
			method: 'POST',
			body: JSON.stringify(obj),
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': getCookie('csrftoken'),
			}
		});
		return response.json();

		function getCookie(name) {
			let cookieValue = null;
			if (document.cookie && document.cookie !== '') {
				const cookies = document.cookie.split(';');
				for (let i = 0; i < cookies.length; i++) {
					const cookie = cookies[i].trim();
					if (cookie.substring(0, name.length + 1) === (name + '=')) {
						cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
						break;
					}
				}
			}
			return cookieValue;
		}
	}

	async function timeout(response, func_true, func_false, delay = global_delay) {
		setTimeout(() => { get_data_in_promise(response, func_true, func_false) }, delay)
	}

	async function get_data_in_promise(promise, success, error) {
		promise.then(data => { return success(data) });
		promise.catch(err => { return error(err) });
	}

	function get_global_url(category) {
		return `http://${window.location.host}/${category}/`
	}

	async function others_func_for_send_and_receive_data(request, url, func_true, func_false) {
		const response = send_data_on_server(request, url);
		await timeout(response, func_true, func_false);
	}

	function check_and_init_session() {
		const session = document.cookie.match(/csrftoken/);
		if (!session) {
			const list_keys = [global_cart, global_currency, global_like];
			const [local_key, category] = ["local", "session"];
			const list_data = {};

			list_keys.forEach(elem => { const data = get_localItem(elem); if (data) { list_data[elem] = data } });

			if (Object.entries(list_data).length) {
				list_data[local_key] = "True";
				const url = get_global_url(category);
				const response = send_data_on_server(list_data, url);
				get_data_in_promise(response, response_valid, response_notvalid);

				function response_valid(data) {
					const elements = data["data"];
					for (let key in elements) {
						const value = elements[key];
						if (key == global_cart) {
							final_set_data(value, value["count"]);
						}
						if (key = global_currency) {
							//set_currency(value)
						}
						set_localItem(value, key);
					}

				}

				function response_notvalid(data) {

				}
			}
		}
	}

	function check_url_for_set_filters() {
		const isNotEmptyFilters = window.location.href.match(/\?(.+)/);
		const name_item = "filters";
		localStorage.removeItem(name_item);
		const max_value = get_localItem("max_price");
		const list_value_slider = [0, max_value, max_value];

		if (isNotEmptyFilters) {
			const filters = {};
			const cls = "choice";
			const list_params = get_url_filters(false, true);
			const list_price = ["min", "max"];
			const list_clr_sz = ["color", "size"];

			for (let key in list_params) {
				const values = list_params[key];
				filters[key] = values;

				if (list_clr_sz.indexOf(key) != -1) {
					values.forEach(elem => { document.querySelector(`[data-id="${elem}"]`).classList.add(cls) });
				}

				if (list_price.indexOf(key) != -1) {
					const index = list_price.indexOf(key);
					list_value_slider[index] = Number(values);
				};
			}


			set_localItem(filters, name_item);
			change_slider(...list_value_slider);
		}
	}

	function get_url_filters(obj, head_mode = false) {
		const url_head = head_mode ? decodeURI(window.location.href) : decodeURI(obj.href);
		const dict_filters = {}
		const list_filters_params = ["query", "category", "size", "min", "max", "color"];

		list_filters_params.forEach(string => {
			const rgxp = new RegExp(`${string}=(.+)`);
			const r_query = url_head.match(rgxp);
			if (r_query) {
				const raw_value = r_query[1].split("&")[0];
				let f_value = raw_value;
				if (["category", "max", "min"].indexOf(string) == -1) {
					const str_split = string == "query" ? "+" : ",";
					f_value = f_value.split(str_split);
				}
				dict_filters[string] = f_value;
			}
		})
		return dict_filters;
	}

	//------------------------------------------------------------------------------------------------------//

	//----------------------------------------localstorage--------------------------------------------------//
	function set_localItem(obj, name_item) {
		const data = JSON.stringify(obj);
		localStorage.setItem(name_item, data);
	}

	function get_localItem(name) {
		const item = localStorage.getItem(name);
		if (item === null) { return false }
		else { return JSON.parse(item) }
	}

	function set_url_no_reload(url) {
		window.history.pushState(null, null, decodeURI(url))
	}
	//------------------------------------------------------------------------------------------------------//

	//---------------------------add_cls_for_one_product_and_unviev_others----------------------------------//
	function init_select_Product() {
		"function for add cls and init select product"
		const selector = "hex"
		const cls = "_down"
		const down_clr = document.querySelector(`[data-${selector}].main-Object__gallery.${cls}`);
		if (down_clr) {
			const hex = down_clr.dataset.hex;
			const list_down = document.querySelectorAll(`[data-${selector}='${hex}']`);
			const list_hex = document.querySelectorAll(`[data-${selector}]`);
			change_cls_for_elements(list_hex, "remove", cls)
			change_cls_for_elements(list_down, "add", cls)
		}
	}
	//------------------------------------------------------------------------------------------------------//

	//-------------------------------------------RangeSlider------------------------------------------------//

	function change_slider(start_v, finish_v, max_range) {
		const rangeSlider = document.querySelector(".range-slider__range");
		rangeSlider.noUiSlider.updateOptions({
			start: [start_v, finish_v], // устанавливаем начальные значения
			range: { // устанавливаем минимальное и максимальное значения
				'min': [0],
				'max': [max_range]
			}
		});
	}

	//-----------------------------------function_for_sum_all_performed_functions---------------------------//
	function performed_function() {
		init_select_Product();
		check_and_init_session();
		general();
		sort_product();
		check_url_for_set_filters();
	}
	//------------------------------------------------------------------------------------------------------//
	//localStorage.clear();


	performed_function();
}