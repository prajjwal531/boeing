package org.meghana.creditcardapi.transactions;

import java.util.List;

import javax.ws.rs.GET;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;
import javax.ws.rs.Produces;
import javax.ws.rs.QueryParam;
import javax.ws.rs.core.MediaType;



@Path("/getData")
public class CreditcardResource {

	@GET
	@Path("/data")
	@Produces(MediaType.TEXT_PLAIN)
	public String getData() {
		return "Hello World";
	}

	@POST
	@Produces(MediaType.TEXT_PLAIN)
	public String getName(@QueryParam("name") String name) {
		return "Hello "+name+" World";

	}


}
