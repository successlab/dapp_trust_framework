// Custom code
be_base_url = "http://localhost:8000/";

function reset_values()
{
    document.getElementById("search_address").innerHTML = "-";
    document.getElementById("individual_trust_score").innerHTML = "...";
    document.getElementById("dapp_trust_score").innerHTML = "...";

    var list = document.getElementById('w3js_links');
    list.innerHTML = '';

    list = document.getElementById('dapp_links');
    list.innerHTML = '';

    var features = ["contains_abi", "avg_gas_price", "median_sender_nonce", "avg_gas_consumed", "avg_trx_freq", "n_unique_incoming_addresses", "returning_user_perc", "n_deployer_transactions", "contains_w3_js"];
    for(var i=0; i<features.length; i++)
    {
        document.getElementById(features[i]).innerHTML = "";
    }
}

function do_a_search() {
    reset_values();
    var searchInput = document.getElementById('search_box_input').value;
    document.getElementById("search_address").innerHTML = searchInput;
    var call_url = be_base_url + "trust_scoring/get_trust_score/?address=" + searchInput;
    fetch(call_url).then((response) => response.json()).then((response_data) => update_values(response_data))
}

function update_values(response_data) {
    // console.log("Search Results: ");
    // console.log(response_data);

    var resp_status = response_data["status"];
    // console.log(resp_status)
    if(resp_status === "Failed")
    {
        update_failed()
    }
    else
    {
        update_table(response_data);
        update_passed(response_data);
        update_w3js_links(response_data);
        update_dapp_links(response_data);
    }
}

function update_failed()
{
    document.getElementById("individual_trust_score").innerHTML = "Invalid Address";
    document.getElementById("individual_trust_score").style = "color: red";
}

function update_passed(response_data)
{
    var individual_score = response_data["contract_trust_score"];
    document.getElementById("individual_trust_score").innerHTML = individual_score;
    if(individual_score >= 75)
    {
        document.getElementById("individual_trust_score").style = "color: green;";
    }
    else if (individual_score >= 25 && individual_score < 75)
    {
        document.getElementById("individual_trust_score").style = "color: orange;";
    }
    else
    {
        document.getElementById("individual_trust_score").style = "color: red;";
    }


    if (isNaN(response_data["dapp_trust_score"]))
    {
        document.getElementById("dapp_trust_score").innerHTML = "Generating...";
    }
    else
    {
        var dapp_score = response_data["dapp_trust_score"].toFixed(2)
        document.getElementById("dapp_trust_score").innerHTML = dapp_score;

        if(dapp_score >= 75)
        {
            document.getElementById("dapp_trust_score").style = "color: green;";
        }
        else if (dapp_score >= 25 && dapp_score < 75)
        {
            document.getElementById("dapp_trust_score").style = "color: orange;";
        }
        else
        {
            document.getElementById("dapp_trust_score").style = "color: red;";
        }
    }

}

function update_table(response_data)
{
    update_limits(response_data);
    update_current_values(response_data);
}

function update_current_values(response_data)
{
    var attribs = response_data["contract_attributes"];

    for(var attrib in attribs)
    {
        // console.log(attrib);
        try
        {
            if(attrib === "contains_abi")
            {
                document.getElementById(attrib).innerHTML = (attribs[attrib])? "Yes": "No";
            }
            else if (attrib === "contains_w3_js")
            {
                document.getElementById(attrib).innerHTML = (attribs[attrib] === 1)? "Yes": "No";
            }
            else
            {
                document.getElementById(attrib).innerHTML = attribs[attrib].toFixed(2);
            }
        }
        catch (e)
        {

        }
    }
}

function update_limits(response_data)
{
    // console.log("Updating the limits");
    var limits = response_data["limits"]["legit_limits"]
    var key_base = "";
    var f = "";
    for(var feature in limits)
    {
        f = feature;
        if(feature === "avg_trx_interval")
        {
            // console.log("Got here")
            f = "avg_trx_freq";
        }
        try
        {
            key_base = f + "_l_";
            document.getElementById(key_base + "25").innerHTML = limits[feature]["25%"].toFixed(2);
            document.getElementById(key_base + "50").innerHTML = limits[feature]["50%"].toFixed(2);
            document.getElementById(key_base + "75").innerHTML = limits[feature]["75%"].toFixed(2);
        }
        catch (e)
        {

        }
    }

    limits = response_data["limits"]["malicious_limits"]
    for(var feature in limits)
    {
        f = feature;
        if(feature === "avg_trx_interval")
        {
            // console.log("Got here")
            f = "avg_trx_freq";
        }
        try
        {
            key_base = f + "_m_";
            document.getElementById(key_base + "25").innerHTML = limits[feature]["25%"].toFixed(2);
            document.getElementById(key_base + "50").innerHTML = limits[feature]["50%"].toFixed(2);
            document.getElementById(key_base + "75").innerHTML = limits[feature]["75%"].toFixed(2);
        }
        catch (e)
        {

        }
    }


    // console.log("Updated the limits");
}

function update_w3js_links(response_data)
{
    // assume API response contains an array of links
    var links = [];
    var w3js_interfaces = response_data["open_source_web3js_interfaces"];

    for (var i = 0; i < w3js_interfaces.length; i++)
    {
        w3js_interface = w3js_interfaces[i];
        // console.log("Interface: " + w3js_interface);
        var title = w3js_interface["user"] + "/" + w3js_interface["repo"];
        var link = w3js_interface["link"];
        var link_parts = link.split("/");
        var file_name = link_parts[link_parts.length - 1];
        title += ": " + file_name;
        links.push([title, link])
    }

    // get a reference to the list element
    const list = document.getElementById('w3js_links');

    // remove any existing list items
    list.innerHTML = '';

    // create and append new list items for each link in the response
    links.forEach(link => {
        const listItem = document.createElement('li');
        listItem.classList.add('list-group-item', 'border-0', 'd-flex', 'justify-content-between', 'ps-0', 'mb-2', 'border-radius-lg');
        listItem.innerHTML = `
            <div class="d-flex align-items-center">
              <div class="d-flex flex-column">
                <a href="${link[1]}">
                    <h6 class="mb-1 text-dark text-sm">${link[0]}</h6>
                </a>
              </div>
            </div>
        `;
        list.appendChild(listItem);
    });
}

function update_dapp_links(response_data)
{
    var links = response_data["dapp_family_links"];
    const list = document.getElementById('dapp_links');

    // remove any existing list items
    list.innerHTML = '';

    if (links === "Generating, check back later")
    {
        list.innerHTML = 'Generating, check back later';
        return;
    }

    // create and append new list items for each link in the response
    for(var link in links)
    {
        var score = links[link]
        var color = "";
        if(score >= 75)
        {
            color = "green";
        }
        else if(score >= 25 && score < 75)
        {
            color = "orange";
        }
        else
        {
            color = "red";
        }

        const listItem = document.createElement('li');
        listItem.classList.add('list-group-item', 'border-0', 'd-flex', 'justify-content-between', 'ps-0', 'mb-2', 'border-radius-lg');
        listItem.innerHTML = `
            <div class="d-flex align-items-center">
                <div class="d-flex flex-column">
                    <h6 class="mb-1 text-dark text-sm">${link}</h6>
                    <span class="text-xs">
                        <span class="font-weight-bold">Trust score: </span>
                        <span style="color: ${color};">${links[link]}</span>
                    </span>
                </div>
            </div>
        `;
        list.appendChild(listItem);
    }
}